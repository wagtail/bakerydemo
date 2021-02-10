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
    title = blocks.CharBlock(required=True)
    content = blocks.RichTextBlock(required=True)

    class Meta:
        icon = "fa-list"


class ExhibitionShortBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    image = ImageChooserBlock()
    start_date = blocks.DateBlock()
    end_date = blocks.DateBlock()

    class Meta:
        icon = "fa-picture-o"


class CardBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock(required=True)
    body = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('button', ButtonBlock()),
        ('accordion', blocks.ListBlock(AccordionBlock())),
        ('link', LinkBlock()),
        ('exhibition', ExhibitionShortBlock())
    ], required=True)

    class Meta:
        icon = "fa-square-o"


class LongBlock(blocks.StructBlock):
    pass


class LogoBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    image = ImageChooserBlock(required=True)
    size = blocks.ChoiceBlock(
        choices=[
            ('large', 'Large'),
            ('small', 'Small')
        ], default='small'
    )

    class Meta:
        icon = "fa-file-image-o"


class LogosBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    logos = blocks.ListBlock(LogoBlock())

    class Meta:
        icon = "fa-file-image-o"


class TabsBlock(blocks.StructBlock):
    pass


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    description = blocks.CharBlock()

    class Meta:
        icon = "fa-picture-o"


class GalleryBlock(blocks.StructBlock):
    style = blocks.ChoiceBlock(
        choices=[
            ('slider', 'Slider'),
            ('carousel', 'Carousel')
        ], default='slider'
    )
    images = blocks.ListBlock(ImageBlock())

    class Meta:
        icon = "fa-picture-o"


class HighlightBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(required=True)
    description = blocks.RichTextBlock(required=True)

    class Meta:
        icon = "fa-bullhorn"

class HighlightsBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    highlights = blocks.ListBlock(HighlightBlock())

    class Meta:
        icon = "fa-bullhorn"


class MuseumMapBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    map_button = ButtonBlock()

    class Meta:
        icon = "fa-map"


class GettingHereBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    body = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('accordion', blocks.ListBlock(AccordionBlock())),
    ], required=True)

    class Meta:
        icon = "fa-location-arrow"


class LandingBlock(blocks.StreamBlock):
    card_sequence = blocks.ListBlock(CardBlock(), icon="fa-list")
    long = LongBlock()
    logos = LogosBlock()
    tabs = TabsBlock()
    gallery = GalleryBlock()
    highlights = HighlightsBlock()
    museum_map = MuseumMapBlock()
    getting_here = GettingHereBlock()
