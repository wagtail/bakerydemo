# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 00:55
from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("breads", "0002_remove_breadsindexpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="breadpage",
            name="body",
            field=wagtail.fields.StreamField(
                (
                    (
                        "heading_block",
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    "heading_text",
                                    wagtail.blocks.CharBlock(
                                        classname="title", required=True
                                    ),
                                ),
                                (
                                    "size",
                                    wagtail.blocks.ChoiceBlock(
                                        blank=True,
                                        choices=[
                                            ("", "Select a header size"),
                                            ("h2", "H2"),
                                            ("h3", "H3"),
                                            ("h4", "H4"),
                                        ],
                                        required=False,
                                    ),
                                ),
                            )
                        ),
                    ),
                    (
                        "paragraph_block",
                        wagtail.blocks.RichTextBlock(
                            icon="pilcrow", template="blocks/paragraph_block.html"
                        ),
                    ),
                    (
                        "image_block",
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    "image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=True
                                    ),
                                ),
                                ("caption", wagtail.blocks.CharBlock(required=False)),
                                (
                                    "attribution",
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            )
                        ),
                    ),
                    (
                        "block_quote",
                        wagtail.blocks.StructBlock(
                            (
                                ("text", wagtail.blocks.TextBlock()),
                                (
                                    "attribute_name",
                                    wagtail.blocks.CharBlock(
                                        blank=True,
                                        label="e.g. Mary Berry",
                                        required=False,
                                    ),
                                ),
                            )
                        ),
                    ),
                    (
                        "embed_block",
                        wagtail.embeds.blocks.EmbedBlock(
                            help_text="Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks",
                            icon="media",
                            template="blocks/embed_block.html",
                        ),
                    ),
                ),
                blank=True,
                verbose_name="Page body",
            ),
        ),
    ]
