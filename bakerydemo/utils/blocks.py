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


class TabsBlock(blocks.StructBlock):
    pass


class GalleryBlock(blocks.StructBlock):
    pass


class HighlightsBlock(blocks.StructBlock):
    pass


class MuseumMapBlock(blocks.StructBlock):
    pass


class GettingHereBlock(blocks.StructBlock):
    pass


class LandingBlock(blocks.StreamBlock):
    card_sequence = blocks.ListBlock(CardBlock(), icon="fa-list")
    long = LongBlock()
    tabs = TabsBlock()
    gallery = GalleryBlock()
    highlights = HighlightsBlock()
    museum_map = MuseumMapBlock()
    getting_here = GettingHereBlock()
