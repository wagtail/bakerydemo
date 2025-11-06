from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.search import index

from bakerydemo.base.blocks import BaseStreamBlock


class PeopleIndexPage(Page):
    """
    Index page for listing all people/team members.
    Similar to BreadsIndexPage but for people.
    """
    introduction = models.TextField(
        help_text="Text to describe the page",
        blank=True
    )
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

    subpage_types = ["people.PersonPage"]
    parent_page_types = ["base.HomePage", "wagtailcore.Page"]
    max_count = 1  # Only allow one People Index Page in the site

    api_fields = [
        APIField("introduction"),
        APIField("image"),
    ]

    class Meta:
        verbose_name = "People Index Page"

    def get_people(self):
        """Returns queryset of live PersonPage objects, most recent first"""
        return (
            PersonPage.objects.live()
            .descendant_of(self)
            .order_by("-first_published_at")
        )

    def children(self):
        """Returns live children for easy access in templates"""
        return self.get_children().specific().live()

    def paginate(self, request, *args):
        """Pagination for the index page"""
        page = request.GET.get("page")
        paginator = Paginator(self.get_people(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        """Add pagination to context"""
        context = super(PeopleIndexPage, self).get_context(request)
        context["people"] = self.paginate(request, self.get_people())
        return context


class PersonPage(Page):
    """
    Individual person/team member detail page.
    Similar to BreadPage but for people profiles.
    """
    first_name = models.CharField("First name", max_length=255)
    last_name = models.CharField("Last name", max_length=255)

    role = models.CharField(
        "Role/Job Title",
        max_length=255,
        help_text="e.g. Lead Developer, Designer, Community Manager"
    )

    introduction = models.TextField(
        help_text="Brief introduction or tagline",
        blank=True
    )

    profile_picture = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Profile photo - square images work best"
    )

    body = StreamField(
        BaseStreamBlock(),
        verbose_name="Biography",
        blank=True,
        use_json_field=True,
        help_text="Full biography with rich content"
    )

    # Social/Contact fields
    email = models.EmailField(blank=True, help_text="Public email address")
    website = models.URLField(blank=True, help_text="Personal website")
    github = models.CharField(
        "GitHub Username",
        max_length=255,
        blank=True,
        help_text="GitHub username (without @)"
    )
    twitter = models.CharField(
        "Twitter/X Handle",
        max_length=255,
        blank=True,
        help_text="Twitter handle (without @)"
    )
    linkedin = models.URLField("LinkedIn Profile", blank=True)

    # Additional fields
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text="City, Country"
    )

    team = models.CharField(
        max_length=100,
        blank=True,
        choices=[
            ("leadership", "Leadership"),
            ("engineering", "Engineering"),
            ("design", "Design"),
            ("community", "Community"),
            ("operations", "Operations"),
            ("contributors", "Contributors"),
        ],
    )

    parent_page_types = ["people.PeopleIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("first_name"),
                FieldPanel("last_name"),
                FieldPanel("role"),
            ],
            heading="Name and Role",
        ),
        FieldPanel("introduction"),
        FieldPanel("profile_picture"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("location"),
                FieldPanel("team"),
            ],
            heading="Organization",
            classname="collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel("email"),
                FieldPanel("website"),
                FieldPanel("github"),
                FieldPanel("twitter"),
                FieldPanel("linkedin"),
            ],
            heading="Contact & Social Media",
            classname="collapsed",
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("first_name"),
        index.SearchField("last_name"),
        index.SearchField("introduction"),
        index.SearchField("body"),
    ]

    api_fields = [
        APIField("first_name"),
        APIField("last_name"),
        APIField("role"),
        APIField("introduction"),
        APIField("profile_picture"),
        APIField("body"),
        APIField("location"),
        APIField("team"),
    ]

    class Meta:
        verbose_name = "Person Page"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        """Returns the person's full name"""
        return f"{self.first_name} {self.last_name}"

