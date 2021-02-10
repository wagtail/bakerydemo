from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.api import APIField
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from bakerydemo.utils.blocks import LandingBlock


class LandingPage(Page):
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    body = StreamField(LandingBlock(),help_text="Page content")

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel("body"),
    ]

    # Export fields over the API
    api_fields = [
        APIField('title'),
        APIField('introduction'),
        APIField('body'),
    ]