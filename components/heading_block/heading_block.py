from django_components import component
from wagtail.blocks import StructBlock, CharBlock, ChoiceBlock

block_name = "heading_block"
template_name = f"{block_name}/{block_name}.html"


# @component.register(block_name)
# class HeadingComponent(component.Component):
#     """HeadingComponent component."""
#
#     template_name = template_name
#
#     class Media:
#         css = f"{block_name}/{block_name}.css"
#         js = f"{block_name}/{block_name}.js"


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
