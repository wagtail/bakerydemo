from datetime import datetime

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index

from bakerydemo.base.blocks import BaseStreamBlock
from bakerydemo.locations.choices import DAY_CHOICES


class OperatingHours(models.Model):
    """
    A Django model to capture operating hours for a Location
    """

    day = models.CharField(max_length=3, choices=DAY_CHOICES, default="MON")
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    closed = models.BooleanField(
        "Closed?", blank=True, help_text="Tick if location is closed on this day"
    )

    api_fields = [
        APIField("day"),
        APIField("get_day_display"),
        APIField("opening_time"),
        APIField("closing_time"),
        APIField("closed"),
    ]

    panels = [
        FieldPanel("day"),
        FieldPanel("opening_time"),
        FieldPanel("closing_time"),
        FieldPanel("closed"),
    ]

    class Meta:
        abstract = True

    def __str__(self):
        if self.opening_time:
            opening = self.opening_time.strftime("%H:%M")
        else:
            opening = "--"
        if self.closing_time:
            closed = self.closing_time.strftime("%H:%M")
        else:
            closed = "--"
        return "{}: {} - {} {}".format(self.day, opening, closed, settings.TIME_ZONE)


class LocationOperatingHours(Orderable, OperatingHours):
    """
    A model creating a relationship between the OperatingHours and Location
    Note that unlike BlogPersonRelationship we don't include a ForeignKey to
    OperatingHours as we don't need that relationship (e.g. any Location open
    a certain day of the week). The ParentalKey is the minimum required to
    relate the two objects to one another. We use the ParentalKey's related_
    name to access it from the LocationPage admin
    """

    location = ParentalKey(
        "LocationPage", related_name="hours_of_operation", on_delete=models.CASCADE
    )


class LocationWeekDaySlot(ClusterableModel, Orderable):
    """
    A model representing a week day slot for nested InlinePanel demonstration.
    This is the parent level that contains multiple hour slots.
    Demonstrates nested InlinePanel functionality for testing expand/collapse
    and scroll issues (related to issue #13352).
    """

    location = ParentalKey(
        "LocationPage", related_name="week_day_slots", on_delete=models.CASCADE
    )
    day = models.CharField(
        max_length=3,
        choices=DAY_CHOICES,
        default="MON",
        help_text="Select the day of the week",
    )

    panels = [
        FieldPanel("day"),
        InlinePanel("hour_slots", heading="Hour Slots", label="Time Slot"),
    ]

    api_fields = [
        APIField("day"),
        APIField("get_day_display"),
        APIField("hour_slots"),
    ]

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Week Day Slot"
        verbose_name_plural = "Week Day Slots"

    def __str__(self):
        return f"{self.get_day_display()}"


class LocationHourSlot(Orderable):
    """
    A model representing individual hour slots within a week day.
    This is the nested/child level of the InlinePanel structure.
    Multiple hour slots can exist per day (e.g., for split shifts).
    """

    week_day_slot = ParentalKey(
        "LocationWeekDaySlot", related_name="hour_slots", on_delete=models.CASCADE
    )
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    closed = models.BooleanField(
        "Closed?",
        default=False,
        blank=True,
        help_text="Tick if location is closed during this time slot",
    )

    panels = [
        FieldPanel("opening_time"),
        FieldPanel("closing_time"),
        FieldPanel("closed"),
    ]

    api_fields = [
        APIField("opening_time"),
        APIField("closing_time"),
        APIField("closed"),
    ]

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Hour Slot"
        verbose_name_plural = "Hour Slots"

    def __str__(self):
        if self.closed:
            return "Closed"
        if self.opening_time and self.closing_time:
            opening = self.opening_time.strftime("%H:%M")
            closing = self.closing_time.strftime("%H:%M")
            return f"{opening} - {closing}"
        return "Time not set"


class LocationsIndexPage(Page):
    """
    A Page model that creates an index page (a listview)
    """

    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and 3000px.",
    )

    # Only LocationPage objects can be added underneath this index page
    subpage_types = ["LocationPage"]

    # Allows children of this indexpage to be accessible via the indexpage
    # object on templates. We use this on the homepage to show featured
    # sections of the site and their child pages
    def children(self):
        return self.get_children().specific().live()

    # Overrides the context to list all child
    # items, that are live, by the title alphabetical order.
    # https://docs.wagtail.org/en/stable/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(LocationsIndexPage, self).get_context(request)
        context["locations"] = (
            LocationPage.objects.descendant_of(self).live().order_by("title")
        )
        return context

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("image"),
    ]

    api_fields = [
        APIField("introduction"),
        APIField("image"),
    ]


class LocationPage(Page):
    """
    Detail for a specific bakery location.
    """

    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and 3000px.",
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True, use_json_field=True
    )
    address = models.TextField()
    lat_long = models.CharField(
        max_length=36,
        help_text="Comma separated lat/long. (Ex. 64.144367, -21.939182) \
                   Right click Google Maps and select 'What's Here'",
        validators=[
            RegexValidator(
                regex=r"^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$",
                message="Lat Long must be a comma-separated numeric lat and long",
                code="invalid_lat_long",
            ),
        ],
    )

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField("address"),
        index.SearchField("body"),
    ]

    # Fields to show to the editor in the admin view
    content_panels = [
        FieldPanel("title"),
        FieldPanel("introduction"),
        FieldPanel("image"),
        FieldPanel("body"),
        FieldPanel("address"),
        FieldPanel("lat_long"),
        InlinePanel(
            "hours_of_operation",
            heading="Hours of Operation (Flat Structure)",
            label="Slot",
        ),
        InlinePanel(
            "week_day_slots",
            heading="Hours of Operation (Nested InlinePanel Demo)",
            label="Day",
            help_text="Demonstration of nested InlinePanel - each day can have multiple time slots",
        ),
    ]

    api_fields = [
        APIField("introduction"),
        APIField("image"),
        APIField("body"),
        APIField("address"),
        APIField("lat_long"),
        APIField("is_open"),
        APIField("hours_of_operation"),
    ]

    def __str__(self):
        return self.title

    @property
    def operating_hours(self):
        hours = self.hours_of_operation.all()
        return hours

    # Determines if the location is currently open. It is timezone naive
    def is_open(self):
        now = datetime.now()
        current_time = now.time()
        current_day = now.strftime("%a").upper()
        try:
            self.operating_hours.get(
                day=current_day,
                opening_time__lte=current_time,
                closing_time__gte=current_time,
                closed=False,
            )
            return True
        except LocationOperatingHours.DoesNotExist:
            return False

    # Makes additional context available to the template so that we can access
    # the latitude, longitude and map API key to render the map
    def get_context(self, request):
        context = super(LocationPage, self).get_context(request)
        context["lat"] = self.lat_long.split(",")[0]
        context["long"] = self.lat_long.split(",")[1]
        context["google_map_api_key"] = settings.GOOGLE_MAP_API_KEY
        return context

    # Can only be placed under a LocationsIndexPage object
    parent_page_types = ["LocationsIndexPage"]
