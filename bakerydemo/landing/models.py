from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page


class LandingPage(Page):
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    body = StreamField(StoryBlock())
    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
    ]
