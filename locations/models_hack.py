from datetime import datetime
import time 
import calendar
import pytz
from pytz import timezone
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.fields import StreamField
#from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable, Page
from wagtail.search import index
#from wagtail.images.edit_handlers import ImageChooserPanel

from bakerydemo.base.blocks import BaseStreamBlock
from bakerydemo.locations.choices import DAY_CHOICES


class OperatingHours(models.Model):
    """
    A Django model to capture operating hours for a Location
    """

    day = models.CharField(
        max_length=4,
        choices=DAY_CHOICES,
        default='MON'
    )
    opening_time = models.TimeField(
        blank=True,
        null=True
    )
    closing_time = models.TimeField(
        blank=True,
        null=True
    )
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
            closed = self.closing_time.strftime('%H:%M')
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
    A model creating a relationship between the OperatingHours and Location
    Note that unlike BlogPeopleRelationship we don't include a ForeignKey to
    OperatingHours as we don't need that relationship (e.g. any Location open
    a certain day of the week). The ParentalKey is the minimum required to
    relate the two objects to one another. We use the ParentalKey's related_
    name to access it from the LocationPage admin
    """
    location = ParentalKey(
        'LocationPage',
        related_name='hours_of_operation',
        on_delete=models.CASCADE
    )


class LocationsIndexPage(Page):
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
    subpage_types = ['LocationPage']

    # Allows children of this indexpage to be accessible via the indexpage
    # object on templates. We use this on the homepage to show featured
    # sections of the site and their child pages
    def children(self):
        return self.get_children().specific().live()

    # Overrides the context to list all child
    # items, that are live, by the date that they were published
    # http://docs.wagtail.io/en/latest/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(LocationsIndexPage, self).get_context(request)
        context['locations'] = LocationPage.objects.descendant_of(
            self).live().order_by(
            'title')
        return context

  #  content_panels = Page.content_panels + [
  #      FieldPanel('introduction', classname="full"),
  #      ImageChooserPanel('image'),
  #  ]
    content_panels = [
        FieldPanel("title"),
        FieldPanel("introduction"),
        FieldPanel("image"),
        FieldPanel("body"),
        FieldPanel("address"),
        FieldPanel("lat_long"),
        InlinePanel("hours_of_operation", heading="Hours of Operation", label="Slot"),
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
    '''
    Maybe call gmaps API with lat/long to get current offset
    https://maps.googleapis.com/maps/api/timezone/json?location=12.9716,77.5946&timestamp=1629304488&key=AIzaSyADY7G9DdLrg8r9m37yGaGJ69kCOtUl_UY
    returns this JSON:
    {
        dstOffset: 0,
        rawOffset: 19800,
        status: "OK",
        timeZoneId: "Asia/Calcutta",
        timeZoneName: "India Standard Time"
    }
    '''
    timezone = models.TextField(
        max_length=25,
        help_text="Examples: US/Pacific, America/Los_Angeles, Etc/UTC",
        default='Etc/UTC',
        validators=[
            RegexValidator(
                regex = r'^(\w+\/?\w+)$',
                message ='Examples: US/Pacific, America/Los_Angeles, Etc/UTC',
                code='invalid_tz'
            )
        ]
    )
    lat_long = models.CharField(
        max_length=36,
        help_text="Comma separated lat/long. (Ex. 64.144367, -21.939182) \
                   Right click Google Maps and select 'What\'s Here'",
        validators=[
            RegexValidator(
                regex=r'^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$',
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

    # Fields to show to the editor in the admin view
    content_panels = [
        FieldPanel('title', classname="full"),
        FieldPanel('introduction', classname="full"),
        FieldPanel('image'),
        FieldPanel('body'),
        FieldPanel('address', classname="full"),
        FieldPanel('timezone', classname="full"),
        FieldPanel('lat_long'),
        InlinePanel("hours_of_operation", heading="Hours of Operation", label="Slot"),
    ]

    def __str__(self):
        return self.title

    @property
    def operating_hours(self):
        hours = self.hours_of_operation.all()
        return hours
       
    # Determines if the location is currently open. It is timezone naive

#        now = datetime.now(pytz.FixedOffset(float(self.timezone)*60))
#        current_time = now.time()
#        current_day = now.strftime('%a').upper()
    def loc_datetime(self):
        cur_zone = pytz.timezone(self.timezone)
        now = datetime.now().astimezone(cur_zone)
        return now.strftime('%a %b %d %Y %H:%M %Z')

    def is_open(self):
        cur_zone = pytz.timezone(self.timezone)
        now = datetime.now().astimezone(cur_zone)
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

    # Makes additional context available to the template so that we can access
    # the latitude, longitude and map API key to render the map
    def get_context(self, request):
        context = super(LocationPage, self).get_context(request)
        context['timezone'] = self.timezone
        context['lat'] = self.lat_long.split(",")[0]
        context['long'] = self.lat_long.split(",")[1]
        context['google_map_api_key'] = settings.GOOGLE_MAP_API_KEY
        return context

    # Can only be placed under a LocationsIndexPage object
    parent_page_types = ['LocationsIndexPage']
