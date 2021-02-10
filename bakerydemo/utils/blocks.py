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
    logo = ImageChooserBlock(required=True)
    size = blocks.ChoiceBlock(
        choices=[
            ('large', 'Large'),
            ('small', 'Small')
        ], default='small'
    )

    class Meta:
        icon = "fa-file-image-o"


class TabsBlock(blocks.StructBlock):
    pass


class GalleryBlock(blocks.StructBlock):
    pass


class HighlightBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(required=True)
    blocks.RichTextBlock(required=True)

    class Meta:
        icon = "fa-bold"


class MuseumMapBlock(blocks.StructBlock):
    map_button = ButtonBlock()

    class Meta:
        icon = "fa-map"


class GettingHereBlock(blocks.StructBlock):
    body = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('accordion', blocks.ListBlock(AccordionBlock())),
    ], required=True)

    class Meta:
        icon = "fa-location-arrow"


class LandingBlock(blocks.StreamBlock):
    card_sequence = blocks.ListBlock(CardBlock(), icon="fa-list")
    long = LongBlock()
    logos = blocks.ListBlock(LogoBlock(), icon="fa-file-image-o")
    tabs = TabsBlock()
    gallery = GalleryBlock()
    highlights = blocks.ListBlock(HighlightBlock())
    museum_map = MuseumMapBlock()
    getting_here = GettingHereBlock()
