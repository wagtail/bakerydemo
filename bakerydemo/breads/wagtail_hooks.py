from django.forms import CheckboxSelectMultiple, RadioSelect
from django.utils.functional import classproperty
from django_filters.filters import ModelChoiceFilter, ModelMultipleChoiceFilter
from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.panels import FieldPanel
from wagtail.admin.ui.tables import Column
from wagtail.admin.views.pages.listing import PageFilterSet
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from bakerydemo.base.filters import RevisionFilterSetMixin
from bakerydemo.breads.models import BreadIngredient, BreadPage, BreadType, Country


class BreadIngredientFilterSet(RevisionFilterSetMixin, WagtailFilterSet):
    class Meta:
        model = BreadIngredient
        fields = {
            "live": ["exact"],
        }


class BreadIngredientSnippetViewSet(SnippetViewSet):
    model = BreadIngredient
    ordering = "name"
    search_fields = ("name",)
    filterset_class = BreadIngredientFilterSet
    inspect_view_enabled = True


class BreadTypeFilterSet(RevisionFilterSetMixin, WagtailFilterSet):
    class Meta:
        model = BreadType
        fields = []


class BreadTypeSnippetViewSet(SnippetViewSet):
    model = BreadType
    ordering = ("title",)
    search_fields = ("title",)
    filterset_class = BreadTypeFilterSet


class CountryModelViewSet(ModelViewSet):
    model = Country
    ordering = "title"
    search_fields = ("title",)
    icon = "globe"
    inspect_view_enabled = True
    sort_order_field = "sort_order"

    panels = [
        FieldPanel("title"),
    ]


class BreadPageFilterSet(PageFilterSet):
    origin = ModelChoiceFilter(queryset=Country.objects.all(), widget=RadioSelect)
    bread_type = ModelMultipleChoiceFilter(
        queryset=BreadType.objects.all(),
        widget=CheckboxSelectMultiple,
    )
    ingredients = ModelMultipleChoiceFilter(
        queryset=BreadIngredient.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = BreadPage
        fields = []


class BreadPageListingViewSet(PageListingViewSet):
    menu_icon = "folder-open-inverse"
    menu_label = "Bread pages"
    model = BreadPage
    filterset_class = BreadPageFilterSet

    @classproperty
    def columns(cls):
        # Replace the parent column with a custom origin column
        origin_column = Column("origin", sort_key="origin", width="12%")
        return [
            col if col.name != "parent" else origin_column for col in super().columns
        ]


# We want to group several snippets together in the admin menu.
# This is done by defining a SnippetViewSetGroup class that contains a list of
# SnippetViewSet classes.
# When using a SnippetViewSetGroup class to group several SnippetViewSet classes together,
# you only need to register the SnippetViewSetGroup class with Wagtail.
# No need to register the individual SnippetViewSet classes.
#
# See the documentation for SnippetViewSet for more details.
# https://docs.wagtail.org/en/stable/reference/viewsets.html#snippetviewsetgroup
class BreadMenuGroup(SnippetViewSetGroup):
    menu_label = "Breads"
    menu_icon = "suitcase"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (
        BreadPageListingViewSet("bread_pages"),
        BreadIngredientSnippetViewSet,
        BreadTypeSnippetViewSet,
        CountryModelViewSet,
    )


register_snippet(BreadMenuGroup)
