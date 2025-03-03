from django import forms
from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    FloatBlock,
    ListBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
)
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageBlock

from bakerydemo.base.blocks import (
    BlockQuote,
    HeadingBlock,
    get_image_api_representation,
)


class CustomImageBlock(ImageBlock):
    def get_api_representation(self, value, context=None):
        data = super().get_api_representation(value, context)
        data["image"] = get_image_api_representation(value)
        return data


class RecipeStepBlock(StructBlock):
    text = RichTextBlock(features=["bold", "italic", "link"])
    difficulty = ChoiceBlock(
        widget=forms.RadioSelect,
        choices=[("S", "Small"), ("M", "Medium"), ("L", "Large")],
        default="S",
    )

    class Meta:
        template = "blocks/recipe_step_block.html"
        icon = "tick"


class RecipeStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """

    heading_block = HeadingBlock(group="Content")
    paragraph_block = RichTextBlock(
        icon="pilcrow", template="blocks/paragraph_block.html", group="Content"
    )
    block_quote = BlockQuote(group="Content")
    table_block = TableBlock(
        group="Content",
        description="A table of data with plain text cells",
        preview_value={
            "first_row_is_table_header": "True",
            "data": [
                ["Bread type", "Origin"],
                ["Anpan", "Japan"],
                ["Crumpet", "United Kingdom"],
                ["Roti buaya", "Indonesia"],
            ],
        },
    )
    typed_table_block = TypedTableBlock(
        [
            ("text", CharBlock()),
            ("numeric", FloatBlock()),
            ("rich_text", RichTextBlock()),
            ("image", CustomImageBlock()),
        ],
        group="Content",
        description=(
            "A table of data with cells that can include "
            "text, numbers, rich text, and images"
        ),
        preview_value={
            "caption": "Nutritional information for 100g of bread",
            "columns": [
                {"type": "rich_text", "heading": "Nutrient"},
                {"type": "numeric", "heading": "White bread"},
                {"type": "numeric", "heading": "Brown bread"},
                {"type": "numeric", "heading": "Wholemeal bread"},
            ],
            "rows": [
                {
                    "values": [
                        '<p><a href="https://en.wikipedia.org/wiki/Protein">'
                        "Protein</a> <b>(g)</b></p>",
                        7.9,
                        7.9,
                        9.4,
                    ]
                },
                {
                    "values": [
                        '<p><a href="https://en.wikipedia.org/wiki/Carbohydrate">'
                        "Carbohydrate</a> <b>(g)</b></p>",
                        46.1,
                        42.1,
                        42,
                    ]
                },
                {
                    "values": [
                        '<p><a href="https://en.wikipedia.org/wiki/Sugar">'
                        "Total sugars</a> <b>(g)</b></p>",
                        3.4,
                        3.4,
                        2.8,
                    ]
                },
            ],
        },
    )

    image_block = CustomImageBlock(group="Media")
    embed_block = EmbedBlock(
        help_text="Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="media",
        template="blocks/embed_block.html",
        group="Media",
        preview_value="https://www.youtube.com/watch?v=mwrGSfiB1Mg",
        description="An embedded video or other media",
    )

    ingredients_list = ListBlock(
        RichTextBlock(features=["bold", "italic", "link"]),
        min_num=2,
        max_num=10,
        icon="list-ol",
        group="Cooking",
        preview_value=["<p>200g flour</p>", "<p>1 egg</p>", "<p>1 cup of sugar</p>"],
        description=(
            "A list of ingredients to use in the recipe "
            "with optional bold, italic, and link options"
        ),
    )
    steps_list = ListBlock(
        RecipeStepBlock(),
        min_num=2,
        max_num=10,
        icon="tasks",
        group="Cooking",
        preview_value=[
            {"text": "<p>An easy step</p>", "difficulty": "S"},
            {"text": "<p>A difficult step</p>", "difficulty": "L"},
            {"text": "<p>A medium step</p>", "difficulty": "M"},
        ],
        description=(
            "A list of steps to follow in the recipe, "
            "with a difficulty rating for each step"
        ),
    )
