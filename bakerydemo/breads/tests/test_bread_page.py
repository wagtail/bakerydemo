from django.test import override_settings
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase
from bakerydemo.breads.models import BreadsIndexPage, BreadPage

@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class BreadsIndexPageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        Site.objects.create(hostname="testserver", root_page=root, is_default_site=True)
        cls.index = BreadsIndexPage(title="Breads", slug="breads", introduction="All our breads")
        root.add_child(instance=cls.index)
        cls.index.save_revision().publish()

    def test_breads_index_renders(self):
        response = self.client.get(self.index.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "breads/breads_index_page.html")
        self.assertContains(response, "All our breads")


@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class BreadPageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        Site.objects.create(hostname="testserver", root_page=root, is_default_site=True)
        cls.index = BreadsIndexPage(title="Breads", slug="breads")
        root.add_child(instance=cls.index)
        cls.index.save_revision().publish()
        cls.page = BreadPage(title="Sourdough", slug="sourdough", introduction="Classic sourdough")
        cls.index.add_child(instance=cls.page)
        cls.page.save_revision().publish()

    def test_bread_page_renders(self):
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "breads/bread_page.html")
        self.assertContains(response, "Sourdough")