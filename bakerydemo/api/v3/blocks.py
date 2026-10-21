"""
Declare the API v3 schema of blocks with a custom ``get_api_representation``.

API v3 documents each StreamField block's value in the OpenAPI schema, but
falls back to an untyped value for any block that overrides
``get_api_representation``, as the output can no longer be inferred from the
block definition.
"""

from typing import Any, TypedDict

from wagtail.api.v3.schemas.generators.read import block_schema_builder
from wagtail.blocks import Block
from wagtail.images.api.fields import ImageRenditionDict

from bakerydemo.base.blocks import CaptionedImageBlock, CustomEmbedBlock
from bakerydemo.recipes.blocks import CustomImageBlock


class StreamFieldImageMeta(TypedDict):
    type: str
    download_url: str
    rendition: ImageRenditionDict


class StreamFieldImage(TypedDict):
    """See ``bakerydemo.base.blocks.get_image_api_representation``."""

    id: int
    title: str
    meta: StreamFieldImageMeta


class EmbedValue(TypedDict):
    url: str
    html: str | None


def _pascal_case(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def struct_block_schema_with(**overrides: Any):
    """
    Like the default StructBlock schema, but with the given child blocks'
    types replaced.
    """

    def func(builder, block: Block, name: str) -> Any:
        name = type(block).__name__
        fields = {
            child_name: overrides[child_name]
            if child_name in overrides
            else builder.get_type(child_block, f"{name}{_pascal_case(child_name)}")
            for child_name, child_block in block.child_blocks.items()
        }
        return builder.get_typed_dict(name, fields)

    return func


def register_block_schemas():
    block_schema_builder.register_block_schema(
        CaptionedImageBlock,
        struct_block_schema_with(image=StreamFieldImage | None),
    )
    block_schema_builder.register_block_schema(
        CustomImageBlock,
        struct_block_schema_with(image=StreamFieldImage | None),
    )
    block_schema_builder.register_block_schema(
        CustomEmbedBlock,
        lambda builder, block, name: EmbedValue,
    )
