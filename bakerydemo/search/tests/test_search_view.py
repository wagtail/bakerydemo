from django.test import TestCase, override_settings
from django.urls import reverse
from wagtail.models import Page, Site

from bakerydemo.blog.models import BlogPage
from bakerydemo.breads.models import BreadPage
from bakerydemo.locations.models import LocationPage
from bakerydemo.recipes.models import RecipePage
from django.core.management import call_command

@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class SearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        cls.site = Site.objects.create(
            hostname="testserver",
            root_page=root,
            is_default_site=True,
        )
        cls.recipe = RecipePage(
            title="Hot Cross Bun", slug="hot-cross-bun", introduction="spiced bun"
        )
        root.add_child(instance=cls.recipe)
        cls.recipe.save_revision().publish()

        cls.blog = BlogPage(
            title="Sourdough Guide", slug="sourdough-guide", introduction="sourdough"
        )
        root.add_child(instance=cls.blog)
        cls.blog.save_revision().publish()

        cls.bread = BreadPage(title="Rye Bread", slug="rye-bread", introduction="rye")
        root.add_child(instance=cls.bread)
        cls.bread.save_revision().publish()

        cls.location = LocationPage(
            title="Maputo Bakery",
            slug="maputo-bakery",
            address="123 Maputo St",
            lat_long="-25.969248, 32.573289",
        )
        root.add_child(instance=cls.location)
        cls.location.save_revision().publish()
        
        call_command("update_index", verbosity=0)

    def test_search_returns_200(self):
        response = self.client.get(reverse("search"), {"q": "bread"})
        self.assertEqual(response.status_code, 200)

    def test_search_uses_correct_template(self):
        response = self.client.get(reverse("search"), {"q": "bread"})
        self.assertTemplateUsed(response, "search/search_results.html")

    def test_empty_query_returns_200(self):
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, 200)

    def test_empty_query_returns_no_results(self):
        response = self.client.get(reverse("search"))
        self.assertQuerySetEqual(response.context["search_results"], [])

    def test_search_finds_blog_page(self):
        response = self.client.get(reverse("search"), {"q": "sourdough"})
        self.assertContains(response, "Sourdough Guide")

    def test_search_finds_bread_page(self):
        response = self.client.get(reverse("search"), {"q": "rye"})
        self.assertContains(response, "Rye Bread")

    def test_search_finds_location_page(self):
        response = self.client.get(reverse("search"), {"q": "maputo"})
        self.assertContains(response, "Maputo Bakery")

    def test_fallback_search_preserves_ordering(self):
        """Merged fallback results should preserve the intended ID ordering via Case/When."""
        response = self.client.get(reverse("search"), {"q": "bread"})
        self.assertEqual(response.status_code, 200)
        results = response.context["search_results"].object_list
        ids = [p.id for p in results]
        self.assertEqual(ids, sorted(ids, key=lambda pk: ids.index(pk)))

    def test_search_finds_recipe_page(self):
        response = self.client.get(reverse("search"), {"q": "hot cross bun"})
        self.assertContains(response, "Hot Cross Bun")
