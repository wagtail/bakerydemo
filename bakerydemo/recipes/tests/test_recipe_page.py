from django.test import override_settings
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase
from bakerydemo.recipes.models import RecipeIndexPage, RecipePage

@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class RecipeIndexPageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        Site.objects.create(hostname="testserver", root_page=root, is_default_site=True)
        cls.index = RecipeIndexPage(title="Recipes", slug="recipes", introduction="All our recipes")
        root.add_child(instance=cls.index)
        cls.index.save_revision().publish()

    def test_recipe_index_renders(self):
        response = self.client.get(self.index.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_index_page.html")
        self.assertContains(response, "All our recipes")


@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class RecipePageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        Site.objects.create(hostname="testserver", root_page=root, is_default_site=True)
        cls.index = RecipeIndexPage(title="Recipes", slug="recipes")
        root.add_child(instance=cls.index)
        cls.index.save_revision().publish()
        cls.page = RecipePage(title="Hot Cross Bun", slug="hot-cross-bun", introduction="Spiced bun")
        cls.index.add_child(instance=cls.page)
        cls.page.save_revision().publish()

    def test_recipe_page_renders(self):
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_page.html")
        self.assertContains(response, "Hot Cross Bun")