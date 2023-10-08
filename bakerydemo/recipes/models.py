from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    HelpPanel,
    MultiFieldPanel,
    MultipleChooserPanel,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index

from bakerydemo.base.blocks import BaseStreamBlock

from .blocks import RecipeStreamBlock


class RecipePersonRelationship(Orderable, models.Model):
    """
    This defines the relationship between the `Person` within the `base`
    app and the RecipePage below. This allows people to be added to a RecipePage.

    We have created a two way relationship between RecipePage and Person using
    the ParentalKey and ForeignKey
    """

    page = ParentalKey(
        "RecipePage",
        related_name="recipe_person_relationship",
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        "base.Person",
        related_name="person_recipe_relationship",
        on_delete=models.CASCADE,
    )
    panels = [FieldPanel("person")]


class RecipePage(Page):
    """
    Recipe pages are more complex than blog pages, demonstrating more advanced StreamField patterns.
    """

    date_published = models.DateField("Date article published", blank=True, null=True)
    subtitle = models.CharField(blank=True, max_length=255)
    introduction = models.TextField(blank=True, max_length=500)
    backstory = StreamField(
        BaseStreamBlock(),
        # Demonstrate block_counts to keep the backstory concise.
        block_counts={
            "heading_block": {"max_num": 1},
            "image_block": {"max_num": 1},
            "embed_block": {"max_num": 1},
        },
        blank=True,
        use_json_field=True,
        help_text="Use only a minimum number of headings and large blocks.",
    )

    # An example of using rich text for single-line content.
    recipe_headline = RichTextField(
        blank=True,
        max_length=120,
        features=["bold", "italic", "link"],
        help_text="Keep to a single line",
    )
    body = StreamField(
        RecipeStreamBlock(),
        blank=True,
        use_json_field=True,
        help_text="The recipe’s step-by-step instructions and any other relevant information.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("date_published"),
        # Using `title` to make a field larger.
        FieldPanel("subtitle", classname="title"),
        MultiFieldPanel(
            [
                # Example use case for HelpPanel.
                HelpPanel(
                    "Refer to keywords analysis and correct international ingredients names to craft the best introduction backstory, and headline."
                ),
                FieldPanel("introduction"),
                # StreamField inside a MultiFieldPanel.
                FieldPanel("backstory"),
                FieldPanel("recipe_headline"),
            ],
            heading="Preface",
        ),
        FieldPanel("body"),
        MultipleChooserPanel(
            "recipe_person_relationship",
            chooser_field_name="person",
            heading="Authors",
            label="Author",
            help_text="Select between one and three authors",
            panels=None,
            min_num=1,
            max_num=3,
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("backstory"),
        index.SearchField("body"),
    ]

    def authors(self):
        """
        Returns the RecipePage's related people. Again note that we are using
        the ParentalKey's related_name from the RecipePersonRelationship model
        to access these objects. This allows us to access the Person objects
        with a loop on the template. If we tried to access the recipe_person_
        relationship directly we'd print `recipe.RecipePersonRelationship.None`
        """
        # Only return authors that are not in draft
        return [
            n.person
            for n in self.recipe_person_relationship.filter(
                person__live=True
            ).select_related("person")
        ]

    # Specifies parent to Recipe as being RecipeIndexPages
    parent_page_types = ["RecipeIndexPage"]

    # Specifies what content types can exist as children of RecipePage.
    # Empty list means that no child content types are allowed.
    subpage_types = []


class RecipeIndexPage(Page):
    """
    Index page for recipe.
    We need to alter the page model's context to return the child page objects,
    the RecipePage objects, so that it works as an index page
    """

    introduction = models.TextField(help_text="Text to describe the page", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
    ]

    # Specifies that only RecipePage objects can live under this index page
    subpage_types = ["RecipePage"]

    # Defines a method to access the children of the page (e.g. RecipePage
    # objects).
    def children(self):
        return self.get_children().specific().live()

    # Overrides the context to list all child items, that are live, by the
    # date that they were published
    # https://docs.wagtail.org/en/stable/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(RecipeIndexPage, self).get_context(request)
        context["recipes"] = (
            RecipePage.objects.descendant_of(self).live().order_by("-date_published")
        )
        return context
