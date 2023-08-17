from __future__ import absolute_import, unicode_literals

import json

from django.conf import settings
from django.forms import widgets
from django.utils import translation
from wagtail.utils.widgets import WidgetWithScript


from wagtail.admin.panels import RichText
from wagtail.rich_text import features

from bakerydemo.tinymce_editor.editor_utils import CustomEditorHTMLConverter


class TinyMCERichTextArea(WidgetWithScript, widgets.Textarea):

    @classmethod
    def getDefaultArgs(cls):
        return {
            'buttons': [
                [
                    ['undo', 'redo', 'nonbreaking'],
                    ['bold', 'italic', 'underline', 'strikethrough', 'formatselect'],
                    ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p'],
                    ['alignleft', 'aligncenter', 'alignright'],
                    ['bullist', 'numlist', 'formats', 'blockformats'],
                    ['wagtaillink', 'unlink'],
                    ['wagtailimage', 'wagtailembed', 'wagtailvideo', 'wagtaildoclink'],
                    ['codeeditor', 'wordcount', 'code'],
                ]
            ],
            'menus': False,
            'options': {
                'browser_spellcheck': True,
                'noneditable_leave_contenteditable': True,
                'language': translation.to_locale(
                    translation.get_language() or settings.LANGUAGE_CODE),
                'language_load': True,
            },
        }

    def __init__(self, attrs=None, **kwargs):
        super(TinyMCERichTextArea, self).__init__(attrs)
        self.kwargs = self.getDefaultArgs()
        self.features = kwargs.pop('features', None)
        if kwargs is not None:
            self.kwargs.update(kwargs)

        if self.features is None:
            self.features = features.get_default_features()
            self.converter = CustomEditorHTMLConverter()

    def get_panel(self):
        return RichText

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            translated_value = None
        else:
            translated_value = self.converter.from_database_format(value)
        return super(TinyMCERichTextArea, self).render(name, translated_value, attrs, renderer)

    def render_js_init(self, id_, name, value):
        kwargs = {
            'options': self.kwargs.get('options', {}),
        }

        if 'buttons' in self.kwargs:
            if self.kwargs['buttons'] is False:
                kwargs['toolbar'] = False
            else:
                kwargs['toolbar'] = [
                    ' | '.join([' '.join(groups) for groups in rows])
                    for rows in self.kwargs['buttons']
                ]

        if 'menus' in self.kwargs:
            if self.kwargs['menus'] is False:
                kwargs['menubar'] = False
            else:
                kwargs['menubar'] = ' '.join(self.kwargs['menus'])

        if 'passthru_init_keys' in self.kwargs:
            kwargs.update(self.kwargs['passthru_init_keys'])

        if 'table' in self.kwargs:
            for key, values in self.kwargs['table'].items():
                kwargs[f'table_{key}'] = values

        return "makeTinyMCEEditable({0}, {1});".format(json.dumps(id_), json.dumps(kwargs))

    def value_from_datadict(self, data, files, name):
        original_value = super(TinyMCERichTextArea, self).value_from_datadict(data, files, name)
        if original_value is None:
            return None
        return self.converter.to_database_format(original_value)


class BotRichTextArea(TinyMCERichTextArea):

    @classmethod
    def getDefaultArgs(cls):
        return {
            'buttons': [
                [
                    ['undo', 'redo'],
                    ['bold', 'italic', 'underline', 'strikethrough', 'formatselect'],
                ]
            ],
            'menus': False,
            'options': {
                'browser_spellcheck': True,
                'noneditable_leave_contenteditable': True,
                'language': translation.to_locale(
                    translation.get_language() or settings.LANGUAGE_CODE),
                'language_load': True,
            },
        }
