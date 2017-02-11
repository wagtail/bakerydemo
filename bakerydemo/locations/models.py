from django.core.validators import RegexValidator
from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


class OperatingHours(models.Model):
    """
    Django model to capture operating hours for a Location
    """
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

    subpage_types = ['LocationPage']

    def get_context(self, request):
        context = super(LocationsIndexPage, self).get_context(request)
        context['locations'] = LocationPage.objects.descendant_of(
            self).live().order_by(
            '-first_published_at')
        return context


class LocationPage(Page):
    """
    Detail for a specific location
    """

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
                   Right click Google Maps and click 'What\'s Here'",
        validators=[
            RegexValidator(
                regex='^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$',
                message='Lat Long must be a comma separated numeric lat and long',
                code='invalid_lat_long'
            ),
        ]
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
        return self.title

    def opening_hours(self):
        hours = self.hours_of_operation.all()
        return hours

    def get_context(self, request):
        context = super(LocationPage, self).get_context(request)
        context['lat'] = self.lat_long.split(",")[0]
        context['long'] = self.lat_long.split(",")[1]
        return context

    parent_page_types = ['LocationsIndexPage']
