from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock as DefaultImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from bakerydemo.base.models import People


class ImageChooserBlock(DefaultImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return {
                "id": value.id,
                "title": value.title,
                "original": value.get_rendition("original").attrs_dict,
            }


class ButtonBlock(blocks.StructBlock):
    label = blocks.CharBlock()
    link = blocks.URLBlock()

    class Meta:
        icon = "fa-play-circle"


class LinkBlock(blocks.StructBlock):
    label = blocks.CharBlock()
    link = blocks.URLBlock()

    class Meta:
        icon = "fa-link"


class AccordionBlock(blocks.StructBlock):
    accordion = blocks.StreamBlock([
        ("accordion", blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('content', blocks.RichTextBlock()),
        ]))
    ])

    class Meta:
        icon = "fa-list"


class CollectionsBlock(blocks.StructBlock):
    collections = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', ImageChooserBlock()),
                ('title', blocks.CharBlock()),
                ('description', blocks.CharBlock()),
                ('artist', SnippetChooserBlock(People)),
                ('year', blocks.IntegerBlock(min_value=0)),
            ]
        )
    )

    class Meta:
        icon = "fa-picture-o"


class EventsBlock(blocks.StructBlock):
    events = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('schedule', blocks.DateTimeBlock()),
                ('Event', blocks.CharBlock()),
                ('description', blocks.CharBlock()),

            ]
        )
    )

    class Meta:
        icon = "fa-street-view"


class ExhibitionCardBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    image = ImageChooserBlock()
    start_date = blocks.DateBlock()
    end_date = blocks.DateBlock()
    body = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('button', ButtonBlock()),
        ('accordion', AccordionBlock()),
        ('link', LinkBlock()),
    ])

    class Meta:
        icon = "fa-picture-o"

    def clean(self, value):
        errors = {}
        if value['start_date'] > value['end_date']:
            errors['start_date'] = ErrorList(['Start date should be less than End Date.'])
            errors['end_date'] = ErrorList(['End date should be greater than Start Date.'])

        if errors:
            raise ValidationError('Validation error in ExhibitionCardBlock', params=errors)

        return super().clean(value)

class StandardCardBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    title = blocks.CharBlock()
    body = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('button', ButtonBlock()),
        ('accordion', AccordionBlock()),
        ('events', EventsBlock()),
        ('link', LinkBlock()),
    ])

    class Meta:
        icon = "fa-square-o"


class LongBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.RichTextBlock()
    body = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('accordion', AccordionBlock()),
        ('collections', CollectionsBlock()),
        ('button', ButtonBlock()),
    ])

    class Meta:
        icon = "fa-arrows-h"


class LogoSequenceBlock(blocks.StructBlock):
    sequence_title = blocks.CharBlock()
    logo_group = blocks.ListBlock(blocks.StructBlock([
        ('sequence_title', blocks.CharBlock()),
        ('logo_sequence', blocks.ListBlock(blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('image', ImageChooserBlock())
        ])))

    ]))

    class Meta:
        icon = "fa-apple"


class TabsBlock(blocks.StructBlock):
    tab_1_title = blocks.CharBlock()
    tab_1_content = blocks.StreamBlock([
        ('accordion', AccordionBlock()),
    ])
    tab_2_content = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('accordion', AccordionBlock()),
    ])

    class Meta:
        icon = "fa-columns"


class GalleryBlock(blocks.StructBlock):
    style = blocks.ChoiceBlock(
        choices=[
            ('slider', 'Slider'),
            ('carousel', 'Carousel')
        ], default='slider'
    )
    images = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', ImageChooserBlock()),
                ('description', blocks.CharBlock()),
            ]
        )
    )

    class Meta:
        icon = "fa-picture-o"


class HighlightWithoutImageBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.StreamBlock([
        ('paragraph', blocks.CharBlock()),
        ('link', LinkBlock()),
    ])
    label = blocks.CharBlock(default="View Details")
    link = blocks.URLBlock()

    class Meta:
        icon = "fa-times"


class HighLightImageBlock(HighlightWithoutImageBlock):
    image = ImageChooserBlock()

    class Meta:
        icon = "fa-check"


class HighlightsWithImageBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    highlights = blocks.ListBlock(HighLightImageBlock())

    class Meta:
        icon = "fa-check"
        label = "Highlights with Image"


class HighlightsWithoutImageBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    highlights = blocks.ListBlock(HighlightWithoutImageBlock())

    class Meta:
        icon = "fa-times"
        label = "Highlights without Image"


class MuseumMapBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    map_button = ButtonBlock()

    class Meta:
        icon = "fa-map"


class GettingHereBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    body = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('accordion', AccordionBlock()),
    ])

    class Meta:
        icon = "fa-location-arrow"


class LandingBlock(blocks.StreamBlock):
    card_sequence = blocks.StreamBlock([
        ('standard', StandardCardBlock()),
        ('exhibition', ExhibitionCardBlock()),
    ], icon="fa-list")
    long = LongBlock()
    logo_sequence = LogoSequenceBlock()
    tabs = TabsBlock()
    gallery = GalleryBlock()
    highlights_with_image = HighlightsWithImageBlock()
    highlights_without_image = HighlightsWithoutImageBlock()
    museum_map = MuseumMapBlock()
    getting_here = GettingHereBlock()
