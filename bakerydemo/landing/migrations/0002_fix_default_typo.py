# Generated by Django 3.1.5 on 2021-02-11 09:59

import bakerydemo.base.models
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpage',
            name='body',
            field=wagtail.core.fields.StreamField([('card_sequence', wagtail.core.blocks.StreamBlock([('standard', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.core.blocks.CharBlock(required=True)), ('body', wagtail.core.blocks.StreamBlock([('paragraph', wagtail.core.blocks.RichTextBlock()), ('button', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=True)), ('link', wagtail.core.blocks.URLBlock(required=True))])), ('accordion', wagtail.core.blocks.StructBlock([('accordion', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('content', wagtail.core.blocks.RichTextBlock(required=True))])))])), ('events', wagtail.core.blocks.StructBlock([('events', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('schedule', wagtail.core.blocks.DateTimeBlock(required=True)), ('Event', wagtail.core.blocks.CharBlock(required=True)), ('description', wagtail.core.blocks.CharBlock(required=True))])))])), ('link', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=True)), ('link', wagtail.core.blocks.URLBlock(required=True))]))], required=True))])), ('exhibition', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('start_date', wagtail.core.blocks.DateBlock()), ('end_date', wagtail.core.blocks.DateBlock()), ('body', wagtail.core.blocks.StreamBlock([('paragraph', wagtail.core.blocks.RichTextBlock()), ('button', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=True)), ('link', wagtail.core.blocks.URLBlock(required=True))])), ('accordion', wagtail.core.blocks.StructBlock([('accordion', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('content', wagtail.core.blocks.RichTextBlock(required=True))])))])), ('link', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=True)), ('link', wagtail.core.blocks.URLBlock(required=True))]))], required=True))]))], icon='fa-list')), ('long', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('description', wagtail.core.blocks.RichTextBlock()), ('body', wagtail.core.blocks.StreamBlock([('paragraph', wagtail.core.blocks.RichTextBlock()), ('accordion', wagtail.core.blocks.StructBlock([('accordion', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('content', wagtail.core.blocks.RichTextBlock(required=True))])))])), ('collections', wagtail.core.blocks.StructBlock([('collections', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.core.blocks.CharBlock(required=True)), ('description', wagtail.core.blocks.CharBlock(required=True)), ('artist', wagtail.snippets.blocks.SnippetChooserBlock(bakerydemo.base.models.People, required=True)), ('year', wagtail.core.blocks.IntegerBlock(min_value=0, required=True))])))])), ('button', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=True)), ('link', wagtail.core.blocks.URLBlock(required=True))]))], required=True))])), ('logo_sequence', wagtail.core.blocks.StructBlock([('sequence_title', wagtail.core.blocks.CharBlock()), ('logo_group', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('sequence_title', wagtail.core.blocks.CharBlock()), ('logo_sequence', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True))])))])))])), ('tabs', wagtail.core.blocks.StructBlock([('tab_1_title', wagtail.core.blocks.CharBlock()), ('tab_1_content', wagtail.core.blocks.StreamBlock([('accordion', wagtail.core.blocks.StructBlock([('accordion', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('content', wagtail.core.blocks.RichTextBlock(required=True))])))]))], required=True)), ('tab_2_content', wagtail.core.blocks.StreamBlock([('paragraph', wagtail.core.blocks.RichTextBlock()), ('accordion', wagtail.core.blocks.StructBlock([('accordion', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('content', wagtail.core.blocks.RichTextBlock(required=True))])))]))], required=True))])), ('gallery', wagtail.core.blocks.StructBlock([('style', wagtail.core.blocks.ChoiceBlock(choices=[('slider', 'Slider'), ('carousel', 'Carousel')])), ('images', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('description', wagtail.core.blocks.CharBlock())])))])), ('highlights_with_image', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('highlights', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('description', wagtail.core.blocks.StreamBlock([('paragraph', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=True)), ('link', wagtail.core.blocks.URLBlock(required=True))]))], required=True)), ('label', wagtail.core.blocks.CharBlock(default='View Details', required=True)), ('link', wagtail.core.blocks.URLBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True))])))])), ('highlights_without_image', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('highlights', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('description', wagtail.core.blocks.StreamBlock([('paragraph', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=True)), ('link', wagtail.core.blocks.URLBlock(required=True))]))], required=True)), ('label', wagtail.core.blocks.CharBlock(default='View Details', required=True)), ('link', wagtail.core.blocks.URLBlock(required=True))])))])), ('museum_map', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('map_button', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=True)), ('link', wagtail.core.blocks.URLBlock(required=True))]))])), ('getting_here', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('body', wagtail.core.blocks.StreamBlock([('paragraph', wagtail.core.blocks.RichTextBlock()), ('accordion', wagtail.core.blocks.StructBlock([('accordion', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('content', wagtail.core.blocks.RichTextBlock(required=True))])))]))], required=True))]))], help_text='Page content'),
        ),
    ]
