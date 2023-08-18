from django import forms
from wagtail.blocks import StructBlock, RichTextBlock, ChoiceBlock
from components.recipe_step import template_name


class RecipeStepBlock(StructBlock):
    text = RichTextBlock(features=["bold", "italic", "link"])
    difficulty = ChoiceBlock(
        widget=forms.RadioSelect,
        choices=[("S", "Small"), ("M", "Medium"), ("L", "Large")],
        default="S",
    )

    class Meta:
        template = template_name
        icon = "tick"
