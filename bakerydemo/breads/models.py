from django import forms
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalManyToManyField

from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from bakerydemo.base.blocks import BaseStreamBlock


@register_snippet
class Country(models.Model):
    """
    Standard Django model to store set of countries of origin.
    Exposed in the Wagtail admin via Snippets.
    """

    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Countries of Origin"


@register_snippet
class BreadIngredient(models.Model):
    """
    Standard Django model used as a Snippet in the BreadPage model.
    Demonstrates ManyToMany relationship.
    """
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Bread ingredients'


@register_snippet
class BreadType(models.Model):
    """
    Standard Django model used as a Snippet in the BreadPage model.
    """

    title = models.CharField(max_length=255)

    panels = [
        FieldPanel('title'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Bread types"


class BreadPage(Page):
    """
    Detail view for a specific bread
    """
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )
    origin = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    bread_type = models.ForeignKey(
        'breads.BreadType',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    ingredients = ParentalManyToManyField('BreadIngredient', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        FieldPanel('origin'),
        FieldPanel('bread_type'),
        MultiFieldPanel(
            [
                FieldPanel(
                    'ingredients',
                    widget=forms.CheckboxSelectMultiple,
                ),
            ],
            heading="Additional Metadata",
            classname="collapsible collapsed"
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('body'),
    ]

    parent_page_types = ['BreadsIndexPage']


class BreadsIndexPage(Page):
    """
    Index page for breads. We don't have any fields within our model but we need
    to alter the page model's context to return the child page objects - the
    BreadPage - so that it works as an index page.
    """

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    subpage_types = ['BreadPage']

    def get_breads(self):
        return BreadPage.objects.live().descendant_of(
            self).order_by('-first_published_at')

    def children(self):
        return self.get_children().specific().live()

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_breads(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super(BreadsIndexPage, self).get_context(request)

        breads = self.paginate(request, self.get_breads())

        context['breads'] = breads

        return context

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
    ]
