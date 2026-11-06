from django.core.cache import cache
from django.test import TestCase
from wagtail.models import Page, Site


class SitemapCacheTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Site.objects.create(
            hostname="testserver",
            root_page=Page.get_first_root_node(),
            is_default_site=True,
        )

    def setUp(self):
        cache.clear()

    def test_sitemap_is_cached(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "max-age=3600")

        with self.assertNumQueries(0):
            response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
