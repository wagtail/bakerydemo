from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ButtonBlock(blocks.StructBlock):
    label = blocks.CharBlock(required=True)
    link = blocks.URLBlock(required=True)

    class Meta:
        icon = "fa-play-circle"


class LinkBlock(blocks.StructBlock):
    label = blocks.CharBlock(required=True)
    link = blocks.URLBlock(required=True)

    class Meta:
        icon = "fa-link"


class AccordionBlock(blocks.StructBlock):
    accordion = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('title', blocks.CharBlock(required=True)),
                ('content', blocks.RichTextBlock(required=True)),
            ]
        )
    )

    class Meta:
        icon = "fa-list"


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
    ], required=True)

    class Meta:
        icon = "fa-picture-o"


class StandardCardBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock(required=True)
    body = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('button', ButtonBlock()),
        ('accordion', AccordionBlock()),
        ('link', LinkBlock()),
    ], required=True)

    class Meta:
        icon = "fa-square-o"


class LongBlock(blocks.StructBlock):
    pass


class LogoSequenceBlock(blocks.StructBlock):
    sequence_title = blocks.CharBlock()
    logos = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('title', blocks.CharBlock()),
                ('image', ImageChooserBlock(required=True)),
                ('size', blocks.ChoiceBlock(choices=[
                    ('large', 'Large'),
                    ('small', 'Small')
                ], default='small')),
            ]
        )
    )

    class Meta:
        icon = "fa-file-image-o"


class TabsBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    pass


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


class HighlightNoImageBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    description = blocks.RichTextBlock(required=True)
    label = blocks.CharBlock(required=True, default="View Detail")
    link = blocks.URLBlock(required=True)

    class Meta:
        icon = "fa-times"


class HightLightImageBlock(HighlightNoImageBlock):
    image = ImageChooserBlock(required=True)

    class Meta:
        icon = "fa-check"


class HighlightsWithImageBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    highlights = blocks.ListBlock(HightLightImageBlock())

    class Meta:
        icon = "fa-check"


class HighlightsWithoutImageBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    highlights = blocks.ListBlock(HighlightNoImageBlock())

    class Meta:
        icon = "fa-times"


class MuseumMapBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    map_button = ButtonBlock()

    class Meta:
        icon = "fa-map"


class GettingHereBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    body = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('accordion', AccordionBlock()),
    ], required=True)

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
