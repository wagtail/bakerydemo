from django.test import override_settings
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase
from bakerydemo.locations.models import LocationsIndexPage, LocationPage

@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class LocationsIndexPageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        Site.objects.create(hostname="testserver", root_page=root, is_default_site=True)
        cls.index = LocationsIndexPage(title="Locations", slug="locations", introduction="Find us here")
        root.add_child(instance=cls.index)
        cls.index.save_revision().publish()

    def test_locations_index_renders(self):
        response = self.client.get(self.index.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/locations_index_page.html")
        self.assertContains(response, "Find us here")


@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class LocationPageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        Site.objects.create(hostname="testserver", root_page=root, is_default_site=True)
        cls.index = LocationsIndexPage(title="Locations", slug="locations")
        root.add_child(instance=cls.index)
        cls.index.save_revision().publish()
        cls.page = LocationPage(
            title="Maputo Bakery",
            slug="maputo-bakery",
            address="123 Maputo St",
            lat_long="-25.969248, 32.573289",
        )
        cls.index.add_child(instance=cls.page)
        cls.page.save_revision().publish()

    def test_location_page_renders(self):
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/location_page.html")
        self.assertContains(response, "Maputo Bakery")