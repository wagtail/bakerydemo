from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


class OperatingHours(models.Model):
    '''
    Django model to capture operating hours for a Location
    '''
    MONDAY = 'MON'
    TUESDAY = 'TUE'
    WEDNESDAY = 'WED'
    THURSDAY = 'THU'
    FRIDAY = 'FRI'
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'

    DAY_CHOICES = (
        (MONDAY, 'MON'),
        (TUESDAY, 'TUE'),
        (WEDNESDAY, 'WED'),
        (THURSDAY, 'THU'),
        (FRIDAY, 'FRI'),
        (SATURDAY, 'SAT'),
        (SUNDAY, 'SUN'),
    )

    day = models.CharField(
        max_length=3,
        choices=DAY_CHOICES,
        default=MONDAY,
    )
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    panels = [
        FieldPanel('day'),
        FieldPanel('opening_time'),
        FieldPanel('closing_time'),
    ]

    class Meta:
        abstract = True

    def __str__(self):
        return '{}: {} - {}'.format(self.day, self.opening_time, self.closing_time)


class LocationOperatingHours(Orderable, OperatingHours):
    '''
    Operating Hours entry for a Location
    '''
    location = ParentalKey(
        'LocationPage',
        related_name='hours_of_operation'
    )


class LocationsLandingPage(Page):
    '''
    Home page for locations
    '''

    pass


class LocationPage(Page):
    '''
    Detail for a specific location
    '''

    address = models.TextField()
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    lat_long = models.CharField(
        max_length=36,
        help_text="Comma separated lat/long. (Ex. 64.144367, -21.939182) \
                   Right click Google Maps and click 'What\'s Here'"


    )

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('address'),
    ]

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('address', classname="full"),
        FieldPanel('lat_long'),
        ImageChooserPanel('image'),
        InlinePanel('hours_of_operation', label="Hours of Operation")
    ]

    def __str__(self):
        return self.name
