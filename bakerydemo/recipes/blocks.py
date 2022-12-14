from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.core.blocks import (
    CharBlock,
    ChoiceBlock,
    FloatBlock,
    ListBlock,
    PageChooserBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
    URLBlock,
)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class RecipeTableBlock(StructBlock):
    title = CharBlock()
    description = TextBlock()
    table = TypedTableBlock(
        [
            ("text", CharBlock()),
            ("numeric", FloatBlock()),
            ("rich_text", RichTextBlock()),
            ("image", ImageChooserBlock()),
        ]
    )


class RecipeStreamBlock(StreamBlock):
    page = PageChooserBlock()
    embed = EmbedBlock()
    image = ImageChooserBlock()


BLOCKS = [
    ("char", CharBlock()),
    (
        "choice",
        ChoiceBlock(choices=[("M", "Medium"), ("L", "Large"), ("XL", "Extra large")]),
    ),
    ("list", ListBlock(child_block=CharBlock())),
    ("page", PageChooserBlock()),
    ("text", TextBlock()),
    ("rich_text", RichTextBlock()),
    ("url", URLBlock()),
    ("document", DocumentChooserBlock()),
    ("embed", EmbedBlock()),
    ("image", ImageChooserBlock()),
    ("table", RecipeTableBlock()),
    ("stream", RecipeStreamBlock()),
]
