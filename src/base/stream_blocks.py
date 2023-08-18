from wagtail.blocks import (
    RichTextBlock,
    StreamBlock,
)
from wagtail.embeds.blocks import EmbedBlock

from components.block_quote.block import BlockQuote
from components.image_block.block import ImageBlock
from components.heading_block.block import HeadingBlock


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """

    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="pilcrow", template="blocks/paragraph_block.html"
    )
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text="Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="media",
        template="blocks/embed_block.html",
    )
