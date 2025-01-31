# Generated by Django 4.2.2 on 2023-06-28 15:39

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("breads", "0006_breadingredient_expire_at_breadingredient_expired_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="breadpage",
            name="questions",
            field=wagtail.fields.StreamField(
                [
                    (
                        "details_block",
                        wagtail.blocks.StructBlock(
                            [
                                ("summary", wagtail.blocks.CharBlock(required=True)),
                                (
                                    "content",
                                    wagtail.blocks.RichTextBlock(required=True),
                                ),
                                (
                                    "open",
                                    wagtail.blocks.BooleanBlock(
                                        default=True,
                                        help_text="Open by default",
                                        label="Open",
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
                use_json_field=True,
                verbose_name="Questions",
            ),
        ),
    ]
