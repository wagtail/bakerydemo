from django.utils.functional import cached_property
from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    ListBlock,
    RichTextBlock,
    StaticBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images import get_image_model
from wagtail.images.blocks import ImageChooserBlock


def get_image_api_representation(image):
    return {
        "id": image.pk,
        "title": image.title,
        "meta": {
            "type": type(image)._meta.label,
            "download_url": image.file.url,
        },
    }


class CaptionedImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """

    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    @cached_property
    def preview_image(self):
        # Cache the image object for previews to avoid repeated queries
        return get_image_model().objects.last()

    def get_preview_value(self):
        return {
            **self.meta.preview_value,
            "image": self.preview_image,
            "caption": self.preview_image.description,
        }

    def get_api_representation(self, value, context=None):
        data = super().get_api_representation(value, context)
        data["image"] = get_image_api_representation(value["image"])
        return data

    class Meta:
        icon = "image"
        template = "blocks/captioned_image_block.html"
        preview_value = {"attribution": "The Wagtail Bakery"}
        description = "An image with optional caption and attribution"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """

    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(
        choices=[
            ("", "Select a header size"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"
        preview_value = {"heading_text": "Healthy bread types", "size": "h2"}
        description = "A heading with level two, three, or four"


class ThemeSettingsBlock(StructBlock):
    theme = ChoiceBlock(
        choices=[
            ("default", "Default"),
            ("highlight", "Highlight"),
        ],
        required=False,
        default="default",
    )
    text_size = ChoiceBlock(
        choices=[
            ("default", "Default"),
            ("large", "Large"),
        ],
        required=False,
        default="default",
    )

    class Meta:
        icon = "cog"
        label_format = "Theme: {theme}, Text size: {text_size}"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """

    text = TextBlock()
    attribute_name = CharBlock(blank=True, required=False, label="e.g. Mary Berry")
    settings = ThemeSettingsBlock(collapsed=True)

    class Meta:
        icon = "openquote"
        template = "blocks/blockquote.html"
        preview_value = {
            "text": (
                "If you read a lot you're well read / "
                "If you eat a lot you're well bread."
            ),
            "attribute_name": "Willie Wagtail",
        }
        description = "A quote with an optional attribution"


class BakerProfileBlock(StructBlock):
    """
    Custom `StructBlock` for a baker profile with optional biographical fields
    """

    name = CharBlock()
    specialty = CharBlock(required=False, label="e.g. Sourdough, Pastry")
    bio = TextBlock(required=False)
    years_baking = CharBlock(required=False, label="e.g. 12 years")
    favourite_loaf = CharBlock(required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = "user"
        template = "blocks/baker_profile_block.html"
        preview_value = {
            "name": "Mary Berry",
            "specialty": "Pastry",
            "bio": (
                "Mary has been baking at the Wagtail Bakery for over a decade. "
                "She trained in Vienna and specialises in laminated doughs."
            ),
            "years_baking": "14 years",
            "favourite_loaf": "Kouign-amann",
        }
        description = "A baker profile with optional biographical details"


class IngredientBlock(StructBlock):
    """
    Custom `StructBlock` for a single recipe ingredient
    """

    name = CharBlock()
    quantity = CharBlock(required=False, label="e.g. 500g, 2 tsp")

    class Meta:
        icon = "list-ul"
        preview_value = {"name": "Strong white flour", "quantity": "500g"}


class RecipeBlock(StructBlock):
    """
    Custom `StructBlock` for a bread recipe with ingredients and baker profile
    """

    title = CharBlock()
    baker = BakerProfileBlock()
    ingredients = ListBlock(IngredientBlock())
    method = RichTextBlock()
    makes = CharBlock(required=False, label="e.g. 1 large loaf, 12 rolls")
    bake_time = CharBlock(required=False, label="e.g. 35–40 minutes at 220°C")
    difficulty = ChoiceBlock(
        choices=[
            ("", "Select a difficulty"),
            ("easy", "Easy"),
            ("medium", "Medium"),
            ("challenging", "Challenging"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "doc-full"
        template = "blocks/recipe_block.html"
        preview_value = {
            "title": "Classic sourdough loaf",
            "makes": "1 large loaf",
            "bake_time": "45 minutes at 230°C",
            "difficulty": "challenging",
        }
        description = "A bread recipe with ingredients, method, and baker profile"


class PageSectionBlock(StructBlock):
    """
    Custom `StructBlock` with a nested StreamBlock for flexible page sections
    """

    heading = CharBlock()
    body = StreamBlock(
        [
            ("text", RichTextBlock(template="blocks/paragraph_block.html")),
            ("image", CaptionedImageBlock()),
            ("quote", BlockQuote()),
        ]
    )
    settings = ThemeSettingsBlock(collapsed=True)

    class Meta:
        icon = "folder-open-inverse"
        template = "blocks/page_section_block.html"
        preview_value = {"heading": "About our bread"}
        description = "A page section with a heading and flexible body content"


class NutritionBlock(StructBlock):
    """
    Custom `StructBlock` for nutritional information per serving
    """

    calories = CharBlock(required=False, label="e.g. 210 kcal")
    carbohydrates = CharBlock(required=False, label="e.g. 42g")
    protein = CharBlock(required=False, label="e.g. 8g")
    fat = CharBlock(required=False, label="e.g. 1g")
    fibre = CharBlock(required=False, label="e.g. 2g")

    class Meta:
        icon = "pick"
        preview_value = {
            "calories": "210 kcal",
            "carbohydrates": "42g",
            "protein": "8g",
            "fat": "1g",
            "fibre": "2g",
        }


class DetailedRecipeBlock(StructBlock):
    """
    Custom `StructBlock` for a bread recipe with nested nutritional information
    """

    recipe = RecipeBlock()
    nutrition = NutritionBlock()
    notes = TextBlock(required=False, label="Baker's notes")

    class Meta:
        icon = "doc-full-inverse"
        template = "blocks/detailed_recipe_block.html"
        preview_value = {
            "notes": (
                "This loaf keeps well for up to three days wrapped in a clean "
                "tea towel. Freeze sliced for up to one month."
            ),
        }
        description = "A bread recipe with nutritional information and baker's notes"


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """

    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="pilcrow",
        template="blocks/paragraph_block.html",
        preview_value=(
            """
            <h2>Our bread pledge</h2>
            <p>As a bakery, <b>breads</b> have <i>always</i> been in our hearts.
            <a href="https://en.wikipedia.org/wiki/Staple_food">Staple foods</a>
            are essential for society, and – bread is the tastiest of all.
            We love to transform batters and doughs into baked goods with a firm
            dry crust and fluffy center.</p>
            """
        ),
        description="A rich text paragraph",
    )
    image_block = CaptionedImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text="Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="media",
        template="blocks/embed_block.html",
        preview_template="base/preview/static_embed_block.html",
        preview_value="https://www.youtube.com/watch?v=mwrGSfiB1Mg",
        description="An embedded video or other media",
    )
    recipe_block = RecipeBlock()
    page_section_block = PageSectionBlock()
    detailed_recipe_block = DetailedRecipeBlock()
    separator_block = StaticBlock(
        admin_text="Horizontal separator — no configuration needed.",
        template="blocks/separator_block.html",
        icon="horizontalrule",
        description="A visual separator between content blocks",
    )