from wagtail.blocks import StructBlock, CharBlock, ChoiceBlock
from components.heading_block import template_name


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
        template = template_name
