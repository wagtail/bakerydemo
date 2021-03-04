from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from wagtail.core import blocks
from wagtail.snippets.blocks import SnippetChooserBlock

from bakerydemo.base.blocks import ImageChooserBlock, RichTextBlock
from bakerydemo.base.models import People


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


class LogoBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    image = ImageChooserBlock()


class LogoSequenceBlock(blocks.StructBlock):
    sequence_title = blocks.CharBlock()
    logos = blocks.StreamBlock([
        ('logo', LogoBlock())
    ])

    class Meta:
        icon = "fa-apple"


class LogoGroupBlock(blocks.StructBlock):
    group_title = blocks.CharBlock()
    logo_sequences = blocks.StreamBlock([
        ('logo_sequence', LogoSequenceBlock())
    ])


class AccordionItemBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    content = RichTextBlock()


class CollectionItemBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock()
    description = blocks.CharBlock()
    artist = SnippetChooserBlock(People)
    year = blocks.IntegerBlock(min_value=0)


class EventItemBlock(blocks.StructBlock):
    schedule = blocks.DateTimeBlock()
    event = blocks.CharBlock()
    description = blocks.CharBlock()


class AccordionBlock(blocks.StructBlock):
    accordion_items = blocks.StreamBlock([
        ("accordion_item", AccordionItemBlock())
    ])

    class Meta:
        icon = "fa-list"


class CollectionBlock(blocks.StructBlock):
    collection_items = blocks.StreamBlock([
        ("collection_item", CollectionItemBlock())
    ])

    class Meta:
        icon = "fa-picture-o"


class EventsBlock(blocks.StructBlock):
    event_items = blocks.StreamBlock([
        ("event_item", EventItemBlock())
    ])

    class Meta:
        icon = "fa-street-view"


class ExhibitionCardBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    image = ImageChooserBlock()
    start_date = blocks.DateBlock()
    end_date = blocks.DateBlock()
    body = blocks.StreamBlock([
        ('paragraph', RichTextBlock()),
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
        ('paragraph', RichTextBlock()),
        ('button', ButtonBlock()),
        ('accordion', AccordionBlock()),
        ('events', EventsBlock()),
        ('link', LinkBlock()),
    ])

    class Meta:
        icon = "fa-square-o"


class LongBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = RichTextBlock()
    body = blocks.StreamBlock([
        ('paragraph', RichTextBlock()),
        ('accordion', AccordionBlock()),
        ('collection', CollectionBlock()),
        ('button', ButtonBlock()),
    ])

    class Meta:
        icon = "fa-arrows-h"


class LogoSequenceBlock(blocks.StructBlock):
    section_title = blocks.CharBlock()
    logo_groups = blocks.StreamBlock([
        ('logo_group', LogoGroupBlock())
    ])

    class Meta:
        icon = "fa-apple"


class TabsBlock(blocks.StructBlock):
    tab_1_title = blocks.CharBlock()
    tab_1_content = blocks.StreamBlock([
        ('accordion', AccordionBlock()),
    ])
    tab_2_content = blocks.StreamBlock([
        ('paragraph', RichTextBlock()),
        ('accordion', AccordionBlock()),
    ])

    class Meta:
        icon = "fa-columns"


class GalleryBlock(blocks.StructBlock):
    STYLE_CHOICES = [
        ('slider', 'Slider'),
        ('carousel', 'Carousel')
    ]
    style = blocks.ChoiceBlock(
        choices=STYLE_CHOICES, default='slider'
    )
    images = blocks.StreamBlock([
        ("image", blocks.StructBlock(
            [
                ('image', ImageChooserBlock()),
                ('description', blocks.CharBlock()),
            ]
        ))
    ])

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
    highlights = blocks.StreamBlock([
        ('image', HighLightImageBlock()),
    ])

    class Meta:
        icon = "fa-check"
        label = "Highlights with Image"


class HighlightsWithoutImageBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    highlights = blocks.StreamBlock([
        ('image', HighlightWithoutImageBlock()),
    ])

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
        ('paragraph', RichTextBlock()),
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
