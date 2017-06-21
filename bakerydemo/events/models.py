from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


class EventPage(Page):
    """
    An Event Page
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
    event_start = models.DateTimeField()
    event_end = models.DateTimeField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        MultiFieldPanel(
            [
                FieldRowPanel([
                    FieldPanel('event_start'),
                    FieldPanel('event_end'),
                ]),
            ],
            heading="Date And Time Information",
        ),
        ImageChooserPanel('image'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('introduction'),
    ]

    # Specifies parent to EventPage as being EventIndexPages
    parent_page_types = ['EventIndexPage']

    # Specifies what content types can exist as children of EventPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []

    def __str__(self):
        return self.title


class EventIndexPage(Page):
    """
    A Page model that creates an index page (a listview)
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

    # Only LocationPage objects can be added underneath this index page
    subpage_types = ['EventPage']

    # Allows children of this indexpage to be accessible via the indexpage
    # object on templates. We use this on the homepage to show featured
    # sections of the site and their child pages
    def children(self):
        return self.get_children().specific().live()

    # Overrides the context to list all child
    # items, that are live, by the date that they were published
    # http://docs.wagtail.io/en/latest/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(EventIndexPage, self).get_context(request)
        context['events'] = EventPage.objects.descendant_of(
            self).live().order_by(
            'title')
        return context

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
    ]
