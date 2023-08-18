from wagtail.blocks import StructBlock, CharBlock
from wagtail.images.blocks import ImageChooserBlock
from components.image_block import template_name


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
