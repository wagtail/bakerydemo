from datetime import datetime

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    StreamFieldPanel)
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailsearch import index

from bakerydemo.base.models import BasePageFieldsMixin
from bakerydemo.base.blocks import BaseStreamBlock


class OperatingHours(models.Model):
    """
    Django model to capture operating hours for a Location
    """
    MONDAY = 'Mon'
    TUESDAY = 'Tue'
    WEDNESDAY = 'Wed'
    THURSDAY = 'Thu'
    FRIDAY = 'Fri'
    SATURDAY = 'Sat'
    SUNDAY = 'Sun'

    DAY_CHOICES = (
        (MONDAY, 'Mon'),
        (TUESDAY, 'Tue'),
        (WEDNESDAY, 'Weds'),
        (THURSDAY, 'Thu'),
        (FRIDAY, 'Fri'),
        (SATURDAY, 'Sat'),
        (SUNDAY, 'Sun'),
    )

    day = models.CharField(
        max_length=4,
        choices=DAY_CHOICES,
        default=MONDAY,
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


class LocationsIndexPage(BasePageFieldsMixin, Page):
    """
    Index page for locations
    """
    subpage_types = ['LocationPage']

    def get_context(self, request):
        context = super(LocationsIndexPage, self).get_context(request)
        context['locations'] = LocationPage.objects.descendant_of(
            self).live().order_by(
            'title')
        return context


class LocationPage(BasePageFieldsMixin, Page):
    """
    Detail for a specific bakery location.
    """
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
    content_panels = BasePageFieldsMixin.content_panels + [
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
        return context

    parent_page_types = ['LocationsIndexPage']
