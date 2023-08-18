from django_components import component

from components.block_quote import css_name, js_name, template_name, block_name


@component.register(block_name)
class HeadingComponent(component.Component):
    """HeadingComponent component."""

    template_name = template_name

    class Media:
        css = css_name
        js = js_name

# class BlockQuote(StructBlock):
#     """
#     Custom `StructBlock` that allows the user to attribute a quote to the author
#     """
#
#     text = TextBlock()
#     attribute_name = CharBlock(blank=True, required=False, label="e.g. Mary Berry")
#
#     class Meta:
#         icon = "openquote"
#         template = "block_quote/block_quote.html"
