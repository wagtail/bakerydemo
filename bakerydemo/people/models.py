from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtail.blocks import StructBlock, ChoiceBlock, URLBlock
from ..breads.models import Country

from bakerydemo.base.blocks import BaseStreamBlock


class SocialMediaBlock(StructBlock):
    """
    Block for social media links
    """

    platform = ChoiceBlock(
        choices=[
            ("github", "GitHub"),
            ("twitter", "Twitter/X"),
            ("linkedin", "LinkedIn"),
            ("instagram", "Instagram"),
            ("facebook", "Facebook"),
            ("mastodon", "Mastodon"),
            ("website", "Personal Website"),
        ],
        help_text="Select the social media platform",
    )
    url = URLBlock(
        help_text="Full URL to your profile (e.g., https://github.com/username)"
    )

    class Meta:
        icon = "link"
        label = "Social Media Link"


class PersonPage(Page):
    """
    Detail view for a specific person
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

    origin = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    social_links = StreamField(
        [("social", SocialMediaBlock())],
        blank=True,
        use_json_field=True,
        help_text="Add social media profiles",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("image"),
        FieldPanel("origin"),
        FieldPanel("body"),
        FieldPanel("social_links"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    parent_page_types = ["PeopleIndexPage"]

    api_fields = [
        APIField("introduction"),
        APIField("image"),
        APIField("body"),
        APIField("origin"),
        APIField("social_links"),
    ]


class PeopleIndexPage(Page):
    """
    Index page for people.

    Lists all People objects with pagination.
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

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("image"),
    ]

    # Can only have PersonPage children
    subpage_types = ["PersonPage"]

    api_fields = [
        APIField("introduction"),
        APIField("image"),
    ]

    # Returns a queryset of PersonPage objects that are live, that are direct
    # descendants of this index page with most recent first
    def get_people(self):
        return (
            PersonPage.objects.live()
            .descendant_of(self)
            .order_by("-first_published_at")
        )

    # Allows child objects (e.g. PersonPage objects) to be accessible via the
    # template
    def children(self):
        return self.get_children().specific().live()

    # Pagination for the index page
    def paginate(self, request, *args):
        page = request.GET.get("page")
        paginator = Paginator(self.get_people(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    # Returns the above to the get_context method that is used to populate the
    # template
    def get_context(self, request):
        context = super(PeopleIndexPage, self).get_context(request)

        # PersonPage objects (get_people) are passed through pagination
        people = self.paginate(request, self.get_people())

        context["people"] = people

        return context
