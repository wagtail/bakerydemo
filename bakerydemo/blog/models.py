from __future__ import unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.wagtailcore.models import Page, Orderable, Collection
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import (
        FieldPanel,
        InlinePanel,
        FieldRowPanel,
        StreamFieldPanel,
        MultiFieldPanel
        )
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from bakerydemo.base.blocks import BaseStreamBlock


class BlogPeopleRelationship(Orderable, models.Model):
    """
    This defines the relationship between the `LocationPage` within the `locations`
    app and the About page below allowing us to add locations to the about
    section.
    """
    page = ParentalKey(
        'BlogPage', related_name='blog_person_relationship'
    )
    people = models.ForeignKey(
        'base.People', related_name='person_blog_relationship'
    )
    panels = [
        SnippetChooserPanel('people')
    ]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')


class BlogPage(Page):
    """
    The About Page
    """
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Location image'
    )

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    date_published = models.DateField("Date article published", blank=True, null=True)

    body = StreamField(
        BaseStreamBlock(), verbose_name="About page detail", blank=True
        )

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        FieldPanel('date_published'),
        InlinePanel(
            'blog_person_relationship', label="Author(s)",
            panels=None, min_num=1),
        FieldPanel('tags'),
    ]

    # def people(self):
    #     people = [
    #          n.people for n in self.person_blog_relationship.all()
    #     ]

    #     return people

    parent_page_types = [
       'BlogIndexPage'
    ]

    # Defining what content type can sit under the parent
    # The empty array means that no children can be placed under the
    # LocationPage page model
    subpage_types = []

    # api_fields = ['image', 'body']


class BlogIndexPage(Page):
    """
    """

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Location listing image'
    )

    introduction = models.TextField(
        help_text='Text to describe the index page',
        blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('introduction')
    ]

    # parent_page_types = [
    #     'home.HomePage'
    # ]

    # Defining what content type can sit under the parent. Since it's a blank
    # array no subpage can be added
    subpage_types = [
        'BlogPage'
    ]

    # api_fields = ['introduction']
