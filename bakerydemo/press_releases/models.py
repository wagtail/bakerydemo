from django.db import models

from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class PressReleaseIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["press_releases.PressReleasePage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["press_releases"] = (
            PressReleasePage.objects.child_of(self).live().order_by("-date")
        )
        return context

    template = "press_releases/press_release_index_page.html"
    parent_page_types = ["base.HomePage"]
class PressReleasePage(Page):
    date = models.DateField("Press release date")
    intro = models.CharField(max_length=300, default="")
    body = RichTextField()
    source = models.CharField(max_length=200, default="")
    contact_email = models.EmailField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("source"),
        FieldPanel("contact_email"),
    ]

    parent_page_types = ["press_releases.PressReleaseIndexPage"]
    subpage_types = []
    template = "press_releases/press_release_page.html"  # ← add this line
    date = models.DateField("Press release date")

    
