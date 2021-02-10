from wagtail.core import blocks


class CardSequenceBlock(blocks.StructBlock):
    pass


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
    card_sequence = CardSequenceBlock()
    long = LongBlock()
    tabs = TabsBlock()
    gallery = GalleryBlock()
    highlights = HighlightsBlock()
    museum_map = MuseumMapBlock()
    getting_here = GettingHereBlock()
