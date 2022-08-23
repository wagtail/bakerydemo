# Generated by Django 3.2.15 on 2022-08-23 16:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import wagtail_editable_help.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('locations', '0005_use_json_field_for_body_streamfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationoperatinghours',
            name='closed',
            field=models.BooleanField(blank=True, help_text=wagtail_editable_help.models.HelpText('Operating hours closed', default='Tick if location is closed on this day'), verbose_name='Closed?'),
        ),
        migrations.AlterField(
            model_name='locationpage',
            name='image',
            field=models.ForeignKey(blank=True, help_text=wagtail_editable_help.models.HelpText('Hero image', default='Landscape mode only; horizontal width between 1000px and 3000px.'), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AlterField(
            model_name='locationpage',
            name='introduction',
            field=models.TextField(blank=True, help_text=wagtail_editable_help.models.HelpText('Location page introduction', default='Text to describe the page')),
        ),
        migrations.AlterField(
            model_name='locationpage',
            name='lat_long',
            field=models.CharField(help_text=wagtail_editable_help.models.HelpText('Location page lat/long', default="Comma separated lat/long. (Ex. 64.144367, -21.939182) Right click Google Maps and select 'What's Here'"), max_length=36, validators=[django.core.validators.RegexValidator(code='invalid_lat_long', message='Lat Long must be a comma-separated numeric lat and long', regex='^(\\-?\\d+(\\.\\d+)?),\\s*(\\-?\\d+(\\.\\d+)?)$')]),
        ),
        migrations.AlterField(
            model_name='locationsindexpage',
            name='image',
            field=models.ForeignKey(blank=True, help_text=wagtail_editable_help.models.HelpText('Hero image', default='Landscape mode only; horizontal width between 1000px and 3000px.'), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AlterField(
            model_name='locationsindexpage',
            name='introduction',
            field=models.TextField(blank=True, help_text=wagtail_editable_help.models.HelpText('Locations index page introduction', default='Text to describe the page')),
        ),
    ]