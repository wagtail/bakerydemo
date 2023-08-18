from django_components import component
from wagtail.blocks import StructBlock, CharBlock
from wagtail.images.blocks import ImageChooserBlock

block_name = "image_block"
template_name = f"{block_name}/{block_name}.html"


@component.register(block_name)
class ImageBlockComponent(component.Component):
    """ImageBlockComponent component."""

    template_name = f"{block_name}/{block_name}.html"

    class Media:
        css = f"{block_name}/{block_name}.css"
        js = f"{block_name}/{block_name}.js"


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """

    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"
        template = template_name
