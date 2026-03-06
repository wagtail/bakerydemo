from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index


class PersonIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = ["PersonPage"]

    class Meta:
        verbose_name = "Person Index Page"

    def get_context(self, request):
        context = super().get_context(request)
        context["people"] = (
            PersonPage.objects.child_of(self).live().order_by("last_name", "first_name")
        )
        return context


class PersonPage(Page):
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    role = models.CharField(max_length=200, default="")
    department = models.CharField(max_length=200, blank=True)
    bio = RichTextField(blank=True)
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    email = models.EmailField(blank=True)
    linkedin_url = models.URLField(blank=True)

    parent_page_types = ["PersonIndexPage"]
    subpage_types = []

    search_fields = Page.search_fields + [
        index.SearchField("first_name"),
        index.SearchField("last_name"),
        index.SearchField("role"),
        index.SearchField("bio"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("first_name"),
                FieldPanel("last_name"),
            ],
            heading="Name",
        ),
        MultiFieldPanel(
            [
                FieldPanel("role"),
                FieldPanel("department"),
            ],
            heading="Role",
        ),
        MultiFieldPanel(
            [
                FieldPanel("photo"),
            ],
            heading="Photo",
        ),
        MultiFieldPanel(
            [
                FieldPanel("bio"),
            ],
            heading="Bio",
        ),
        MultiFieldPanel(
            [
                FieldPanel("email"),
                FieldPanel("linkedin_url"),
            ],
            heading="Contact",
        ),
    ]

    class Meta:
        verbose_name = "Person Page"

