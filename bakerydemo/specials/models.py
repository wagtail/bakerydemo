from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page

from .blocks import BLOCKS


class SpecialPage(Page):
    """
    SpecialPage, to illustrate some special Wagtail scenario's
    """

    title_1 = models.CharField(max_length=255, default="Title 1")
    section_1 = StreamField(
        BLOCKS,
        blank=True,
        use_json_field=True,
        help_text="Section 1 is a StreamField in a regular FieldPanel",
    )
    title_2 = models.CharField(max_length=255, default="Title 2")
    section_2 = StreamField(
        BLOCKS,
        blank=True,
        use_json_field=True,
        help_text="Section 2 is a StreamField in a MultiFieldPanel",
    )

    content_panels = Page.content_panels + [
        FieldPanel("title_1"),
        FieldPanel("section_1"),
        MultiFieldPanel(
            [
                FieldPanel("title_2"),
                FieldPanel("section_2"),
            ],
            heading="MultiFieldPanel for section 2",
        ),
        InlinePanel(
            "items", label="Items", help_text="Related items via an inline panel"
        ),
    ]


class Item(Orderable):
    page = ParentalKey(SpecialPage, on_delete=models.CASCADE, related_name="items")
    title_1 = models.CharField(max_length=255, default="Title 1")
    section_1 = StreamField(
        BLOCKS,
        blank=True,
        use_json_field=True,
        help_text="Section 1 is a StreamField in a regular FieldPanel",
    )
    title_2 = models.CharField(max_length=255, default="Title 2")
    section_2 = StreamField(
        BLOCKS,
        blank=True,
        use_json_field=True,
        help_text="Section 2 is a StreamField in a MultiFieldPanel",
    )

    panels = [
        FieldPanel("title_1"),
        FieldPanel("section_1"),
        MultiFieldPanel(
            [
                FieldPanel("title_2"),
                FieldPanel("section_2"),
            ],
            heading="MultiFieldPanel for section 2",
        ),
    ]
