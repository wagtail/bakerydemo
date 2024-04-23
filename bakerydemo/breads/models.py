from django import forms
from django.contrib.contenttypes.fields import GenericRelation
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import DraftStateMixin, Page, RevisionMixin
from wagtail.search import index

from bakerydemo.base.blocks import BaseStreamBlock


class Country(models.Model):
    """
    A Django model to store set of countries of origin.
    It is made accessible in the Wagtail admin interface through the CountrySnippetViewSet
    class in wagtail_hooks.py. This allows us to customize the admin interface for this snippet.
    In the BreadPage model you'll see we use a ForeignKey to create the relationship between
    Country and BreadPage. This allows a single relationship (e.g only one
    Country can be added) that is one-way (e.g. Country will have no way to
    access related BreadPage objects).
    """

    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "country of origin"
        verbose_name_plural = "countries of origin"


class BreadIngredient(DraftStateMixin, RevisionMixin, models.Model):
    """
    A Django model to store a single ingredient.
    It is made accessible in the Wagtail admin interface through the BreadIngredientSnippetViewSet
    class in wagtail_hooks.py. This allows us to customize the admin interface for this snippet.
    We use a piece of functionality available to Wagtail called the ParentalManyToManyField on the BreadPage
    model to display this. The Wagtail Docs give a slightly more detailed example
    https://docs.wagtail.org/en/stable/getting_started/tutorial.html#categories
    """

    name = models.CharField(max_length=255)

    revisions = GenericRelation(
        "wagtailcore.Revision",
        content_type_field="base_content_type",
        object_id_field="object_id",
        related_query_name="bread_ingredient",
        for_concrete_model=False,
    )

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "bread ingredient"
        verbose_name_plural = "bread ingredients"


class BreadType(RevisionMixin, models.Model):
    """
    A Django model to define the bread type
    It is made accessible in the Wagtail admin interface through the BreadTypeSnippetViewSet
    class in wagtail_hooks.py. This allows us to customize the admin interface for this snippet.
    In the BreadPage model you'll see we use a ForeignKey
    to create the relationship between BreadType and BreadPage. This allows a
    single relationship (e.g only one BreadType can be added) that is one-way
    (e.g. BreadType will have no way to access related BreadPage objects)
    """

    title = models.CharField(max_length=255)

    revisions = GenericRelation(
        "wagtailcore.Revision",
        content_type_field="base_content_type",
        object_id_field="object_id",
        related_query_name="bread_type",
        for_concrete_model=False,
    )

    panels = [
        FieldPanel("title"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "bread type"
        verbose_name_plural = "bread types"


class BreadPage(Page):
    """
    Detail view for a specific bread
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

    # We include related_name='+' to avoid name collisions on relationships.
    # e.g. there are two FooPage models in two different apps,
    # and they both have a FK to bread_type, they'll both try to create a
    # relationship called `foopage_objects` that will throw a valueError on
    # collision.
    bread_type = models.ForeignKey(
        "breads.BreadType",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    ingredients = ParentalManyToManyField("BreadIngredient", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("image"),
        FieldPanel("body"),
        FieldPanel("origin"),
        FieldPanel("bread_type"),
        MultiFieldPanel(
            [
                FieldPanel(
                    "ingredients",
                    widget=forms.CheckboxSelectMultiple,
                ),
            ],
            heading="Additional Metadata",
            classname="collapsed",
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    parent_page_types = ["BreadsIndexPage"]


class BreadsIndexPage(Page):
    """
    Index page for breads.

    This is more complex than other index pages on the bakery demo site as we've
    included pagination. We've separated the different aspects of the index page
    to be discrete functions to make it easier to follow
    """

    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and " "3000px.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("image"),
    ]

    # Can only have BreadPage children
    subpage_types = ["BreadPage"]

    # Returns a queryset of BreadPage objects that are live, that are direct
    # descendants of this index page with most recent first
    def get_breads(self):
        return (
            BreadPage.objects.live().descendant_of(self).order_by("-first_published_at")
        )

    # Allows child objects (e.g. BreadPage objects) to be accessible via the
    # template. We use this on the HomePage to display child items of featured
    # content
    def children(self):
        return self.get_children().specific().live()

    # Pagination for the index page. We use the `django.core.paginator` as any
    # standard Django app would, but the difference here being we have it as a
    # method on the model rather than within a view function
    def paginate(self, request, *args):
        page = request.GET.get("page")
        paginator = Paginator(self.get_breads(), 12)
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
        context = super(BreadsIndexPage, self).get_context(request)

        # BreadPage objects (get_breads) are passed through pagination
        breads = self.paginate(request, self.get_breads())

        context["breads"] = breads

        return context
