import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel, model_from_serializable_data
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.fields import StreamField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.models import Orderable, Page
from wagtail.search import index

from bakerydemo.base.blocks import BaseStreamBlock
from bakerydemo.locations.choices import DAY_CHOICES


class LocationOperatingDay(Orderable, ClusterableModel):
    """
    A day of the week on which a Location has operating hours. Each day holds
    its own time slots (e.g. to allow for a lunch break), which are edited
    with an InlinePanel nested inside the LocationPage's InlinePanel. To be
    used as the parent of a nested InlinePanel, the model must be a
    ClusterableModel.
    """

    location = ParentalKey(
        "LocationPage", related_name="hours_of_operation", on_delete=models.CASCADE
    )
    day = models.CharField(max_length=3, choices=DAY_CHOICES, default="MON")
    closed = models.BooleanField(
        "Closed?",
        default=False,
        blank=True,
        help_text="Tick if location is closed on this day",
    )

    api_fields = [
        APIField("day"),
        APIField("get_day_display"),
        APIField("closed"),
        APIField("time_slots"),
    ]

    panels = [
        FieldPanel("day"),
        FieldPanel("closed"),
        InlinePanel("time_slots", heading="Opening hours", label="Time slot"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "operating day"

    def __str__(self):
        if self.closed:
            hours = "Closed"
        else:
            hours = ", ".join(str(slot) for slot in self.time_slots.all()) or "--"
        return f"{self.day}: {hours} {settings.TIME_ZONE}"


class LocationOperatingTimeSlot(Orderable):
    """
    An opening and closing time within a LocationOperatingDay. The ParentalKey
    to LocationOperatingDay is what allows it to be edited with a nested
    InlinePanel.

    This model also uses a custom UUID primary key (rather than Django's default
    auto-incrementing `id`) to demonstrate that InlinePanel works with
    non-default primary keys.
    """

    # The UUID is assigned on save rather than with a field default. With a
    # default, unsaved time slots in a draft revision would already have a
    # primary key, which makes them look like existing database rows when the
    # revision is loaded back into the edit form.
    uuid = models.UUIDField(primary_key=True, editable=False)
    day = ParentalKey(
        "LocationOperatingDay", related_name="time_slots", on_delete=models.CASCADE
    )
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    api_fields = [
        APIField("opening_time"),
        APIField("closing_time"),
    ]

    panels = [
        FieldPanel("opening_time"),
        FieldPanel("closing_time"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "time slot"

    def __str__(self):
        opening = self.opening_time.strftime("%H:%M")
        closing = self.closing_time.strftime("%H:%M")
        return f"{opening} - {closing}"

    @classmethod
    def from_serializable_data(cls, data, check_fks=True, strict_fks=False):
        # When loading a revision, modelcluster sets the primary key from the
        # JSON data as-is, i.e. as a string rather than a UUID. Convert it so
        # that the edit form can match it to the submitted time slot.
        obj = model_from_serializable_data(
            cls, data, check_fks=check_fks, strict_fks=strict_fks
        )
        if obj is not None:
            obj.pk = cls._meta.pk.to_python(obj.pk)
        return obj

    def save(self, *args, **kwargs):
        if self.uuid is None:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if (
            self.opening_time
            and self.closing_time
            and self.opening_time >= self.closing_time
        ):
            raise ValidationError(
                {"closing_time": "Closing time must be after opening time."}
            )


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
        context = super().get_context(request)
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
        InlinePanel("hours_of_operation", heading="Hours of Operation", label="Day"),
    ]

    api_fields = [
        APIField("introduction"),
        APIField("image"),
        APIField("body"),
        APIField("address"),
        APIField("lat_long"),
        APIField("is_open"),
        APIField("hours_of_operation"),
        APIField(
            "image_hero",
            serializer=ImageRenditionField("fill-1920x600", source="image"),
        ),
        APIField(
            "image_location_card",
            serializer=ImageRenditionField("fill-430x320", source="image"),
        ),
        APIField(
            "image_picture_card",
            serializer=ImageRenditionField("fill-645x480", source="image"),
        ),
    ]

    def __str__(self):
        return self.title

    @property
    def operating_hours(self):
        hours = self.hours_of_operation.all()
        return hours

    # Determines if the location is currently open.
    # This iterates over the related objects in Python rather than querying
    # the database, so that it also works with unsaved data in previews.
    def is_open(self):
        now = timezone.localtime()
        current_time = now.time()
        current_day = now.strftime("%a").upper()
        for operating_day in self.operating_hours:
            if operating_day.day != current_day or operating_day.closed:
                continue
            for slot in operating_day.time_slots.all():
                if slot.opening_time <= current_time <= slot.closing_time:
                    return True
        return False

    # Makes additional context available to the template so that we can access
    # the latitude, longitude and map API key to render the map
    def get_context(self, request):
        context = super().get_context(request)
        context["lat"] = self.lat_long.split(",")[0]
        context["long"] = self.lat_long.split(",")[1]
        context["google_map_api_key"] = settings.GOOGLE_MAP_API_KEY
        return context

    # Can only be placed under a LocationsIndexPage object
    parent_page_types = ["LocationsIndexPage"]
