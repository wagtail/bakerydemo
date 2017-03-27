from datetime import datetime

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel

from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from bakerydemo.base.blocks import BaseStreamBlock
from bakerydemo.locations.choices import DAY_CHOICES


class OperatingHours(models.Model):
    """
    Django model to capture operating hours for a Location
    """

    day = models.CharField(
        max_length=4,
        choices=DAY_CHOICES,
        default='MON'
    )
    opening_time = models.TimeField(
        blank=True,
        null=True)
    closing_time = models.TimeField(
        blank=True,
        null=True)
    closed = models.BooleanField(
        "Closed?",
        blank=True,
        help_text='Tick if location is closed on this day'
    )

    panels = [
        FieldPanel('day'),
        FieldPanel('opening_time'),
        FieldPanel('closing_time'),
        FieldPanel('closed'),
    ]

    class Meta:
        abstract = True

    def __str__(self):
        if self.opening_time:
            opening = self.opening_time.strftime('%H:%M')
        else:
            opening = '--'
        if self.closing_time:
            closed = self.opening_time.strftime('%H:%M')
        else:
            closed = '--'
        return '{}: {} - {} {}'.format(
            self.day,
            opening,
            closed,
            settings.TIME_ZONE
        )


class LocationOperatingHours(Orderable, OperatingHours):
    """
    Operating Hours entry for a Location
    """
    location = ParentalKey(
        'LocationPage',
        related_name='hours_of_operation'
    )


class LocationsIndexPage(Page):
    """
    Index page for locations
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

    subpage_types = ['LocationPage']

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(LocationsIndexPage, self).get_context(request)
        context['locations'] = LocationPage.objects.descendant_of(
            self).live().order_by(
            'title')
        return context

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
    ]


class LocationPage(Page):
    """
    Detail for a specific bakery location.
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
    address = models.TextField()
    lat_long = models.CharField(
        max_length=36,
        help_text="Comma separated lat/long. (Ex. 64.144367, -21.939182) \
                   Right click Google Maps and select 'What\'s Here'",
        validators=[
            RegexValidator(
                regex='^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$',
                message='Lat Long must be a comma-separated numeric lat and long',
                code='invalid_lat_long'
            ),
        ]
    )

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField('address'),
        index.SearchField('body'),
    ]

    # Editor panels configuration
    content_panels = [
        FieldPanel('title', classname="full"),
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        FieldPanel('address', classname="full"),
        FieldPanel('lat_long'),
        InlinePanel('hours_of_operation', label="Hours of Operation"),
    ]

    def __str__(self):
        return self.title

    @property
    def operating_hours(self):
        hours = self.hours_of_operation.all()
        return hours

    def is_open(self):
        # Determines if the location is currently open
        now = datetime.now()
        current_time = now.time()
        current_day = now.strftime('%a').upper()
        try:
            self.operating_hours.get(
                day=current_day,
                opening_time__lte=current_time,
                closing_time__gte=current_time
            )
            return True
        except LocationOperatingHours.DoesNotExist:
            return False

    def get_context(self, request):
        context = super(LocationPage, self).get_context(request)
        context['lat'] = self.lat_long.split(",")[0]
        context['long'] = self.lat_long.split(",")[1]
        context['google_map_api_key'] = settings.GOOGLE_MAP_API_KEY
        return context

    parent_page_types = ['LocationsIndexPage']
