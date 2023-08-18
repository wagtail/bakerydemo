from wagtail.whitelist import check_url
from wagtail.admin.rich_text.converters.editor_html import EditorHTMLConverter, DbWhitelister
from django.utils.functional import cached_property


def additional_validation_rule(validation_attrs):
    """
    Allow all attrs.
    If attr has rule - replace the attribute with the result of calling
    Otherwise, keep the attribute
    """
    def fn(tag):
        for attr, val in list(tag.attrs.items()):
            rule = validation_attrs.get(attr)
            if rule:
                if callable(rule):
                    new_val = rule(val)
                    if new_val is None:
                        del tag[attr]
                    else:
                        tag[attr] = new_val
                else:
                    pass
            else:
                if rule is False:
                    del tag[attr]
                pass
    return fn


allow_all_attributes = additional_validation_rule({})


CUSTOM_DEFAULT_ELEMENT_RULES = {
    '[document]': allow_all_attributes,
    'a': additional_validation_rule({'href': check_url}),
    'b': allow_all_attributes,
    'br': allow_all_attributes,
    'div': allow_all_attributes,
    'em': allow_all_attributes,
    'h1': allow_all_attributes,
    'h2': allow_all_attributes,
    'h3': allow_all_attributes,
    'h4': allow_all_attributes,
    'h5': allow_all_attributes,
    'h6': allow_all_attributes,
    'hr': allow_all_attributes,
    'i': allow_all_attributes,
    'img': additional_validation_rule({'src': check_url}),
    'li': allow_all_attributes,
    'ol': allow_all_attributes,
    'p': allow_all_attributes,
    'strong': allow_all_attributes,
    'sub': allow_all_attributes,
    'sup': allow_all_attributes,
    'ul': allow_all_attributes,
    'video': additional_validation_rule({'width': False, 'height': False}),
    'source': allow_all_attributes,
    'picture': allow_all_attributes,
    'span': allow_all_attributes,
    'iframe': allow_all_attributes,
    'u': allow_all_attributes,
}


class CustomDbWhiteLister(DbWhitelister):
    element_rules = CUSTOM_DEFAULT_ELEMENT_RULES

    def __init__(self, converter_rules):
        super(CustomDbWhiteLister, self).__init__(converter_rules)
        self.element_rules = CUSTOM_DEFAULT_ELEMENT_RULES.copy()

    def clean_tag_node(self, doc, tag):
        if 'data-embedtype' in tag.attrs:
            embed_type = tag['data-embedtype']
            # fetch the appropriate embed handler for this embedtype
            try:
                embed_handler = self.embed_handlers[embed_type]
            except KeyError:
                # discard embeds with unrecognised embedtypes
                tag.decompose()
                return

            embed_attrs = embed_handler.get_db_attributes(tag)
            embed_attrs['embedtype'] = embed_type

            embed_tag = doc.new_tag('embed', **embed_attrs)
            embed_tag.can_be_empty_element = True
            tag.replace_with(embed_tag)
        elif tag.name == 'a' and 'data-linktype' in tag.attrs:
            for child in tag.contents:
                self.clean_node(doc, child)

            link_attrs = {'href': tag.attrs['href']}
            tag.attrs.clear()
            tag.attrs.update(**link_attrs)
        else:
            super(DbWhitelister, self).clean_tag_node(doc, tag)


class CustomEditorHTMLConverter(EditorHTMLConverter):
    @cached_property
    def whitelister(self):
        return CustomDbWhiteLister(self.converter_rules)
