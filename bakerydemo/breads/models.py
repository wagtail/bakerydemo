
from django.db import models


from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel

from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailcore import blocks
from wagtail.wagtailsnippets.models import register_snippet


@register_snippet
class Country(models.Model):
    '''
    Standard Django model to store set of countries of origin.
    Exposed in the Wagtail admin via Snippets.
    '''

    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Countries of Origin"


class BreadsIndexPage(Page):
    '''
    Home page for breads. Nothing needed in the model here - we'll just
    create an instance, then pull its children into the template.
    '''

    subpage_types = ['BreadPage']


@register_snippet
class BreadType(models.Model):
    '''
    Standard Django model used as a Snippet in the BreadPage model.
    '''

    title = models.CharField(max_length=255)

    panels = [
        FieldPanel('title'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Bread types"


class BreadPage(Page):
    '''
    Detail view for a specific bread
    '''

    origin = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        )
    description = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
    ])
    bread_type = models.ForeignKey(
        'breads.BreadType',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    content_panels = [
        FieldPanel('title'),
        FieldPanel('origin'),
        FieldPanel('bread_type'),
        ImageChooserPanel('image'),
        StreamFieldPanel('description'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('description'),
    ]

    parent_page_types = [
       'BreadsIndexPage'
    ]
