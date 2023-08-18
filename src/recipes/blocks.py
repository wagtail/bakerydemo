from wagtail.blocks import (
    CharBlock,
    FloatBlock,
    ListBlock,
    RichTextBlock,
    StreamBlock,
)
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from components.block_quote.block import BlockQuote
from components.heading_block.block import HeadingBlock
from components.image_block.block import ImageBlock
from components.recipe_step.block import RecipeStepBlock


class RecipeStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """

    heading_block = HeadingBlock(group="Content")
    paragraph_block = RichTextBlock(
        icon="pilcrow", template="blocks/paragraph_block.html", group="Content"
    )
    block_quote = BlockQuote(group="Content")
    table_block = TableBlock(group="Content")
    typed_table_block = TypedTableBlock(
        [
            ("text", CharBlock()),
            ("numeric", FloatBlock()),
            ("rich_text", RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        group="Content",
    )

    image_block = ImageBlock(group="Media")
    embed_block = EmbedBlock(
        help_text="Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="media",
        template="blocks/embed_block.html",
        group="Media",
    )

    ingredients_list = ListBlock(
        RichTextBlock(features=["bold", "italic", "link"]),
        min_num=2,
        max_num=10,
        icon="list-ol",
        group="Cooking",
    )
    steps_list = ListBlock(
        RecipeStepBlock(),
        min_num=2,
        max_num=10,
        icon="tasks",
        group="Cooking",
    )
