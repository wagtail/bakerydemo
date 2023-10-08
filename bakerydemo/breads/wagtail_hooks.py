from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from bakerydemo.breads.models import BreadIngredient, BreadType, Country


class BreadIngredientSnippetViewSet(SnippetViewSet):
    model = BreadIngredient
    ordering = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True


class BreadTypeSnippetViewSet(SnippetViewSet):
    model = BreadType
    ordering = ("title",)
    search_fields = ("title",)


class CountrySnippetViewSet(SnippetViewSet):
    model = Country
    ordering = ("title",)
    search_fields = ("title",)


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
    menu_label = "Bread Categories"
    menu_icon = "suitcase"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (
        BreadIngredientSnippetViewSet,
        BreadTypeSnippetViewSet,
        CountrySnippetViewSet,
    )


register_snippet(BreadMenuGroup)
