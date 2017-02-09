from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from .blocks import FormPageBlock
from core.models import SiteSettingsTemplateMixin


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPage(SiteSettingsTemplateMixin, AbstractEmailForm):
    header_image = models.ForeignKey(
        'core.OvercastImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(FormPageBlock())
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel('header_image'),
        StreamFieldPanel('body'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
