from django.test import override_settings
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from bakerydemo.base.models import HomePage


@override_settings(
    STORAGES={
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        }
    }
)
class HomePageRenderTest(WagtailPageTestCase):
    """
    Tests that the HomePage cam render correctly
    """

    def test_homepage_renders(self):
        # Setup: Create the page tree and site
        root = Page.get_first_root_node()
        Site.objects.create(
            hostname="testserver",
            root_page=root,
            is_default_site=True,
        )

        # Create and publish the HomePage
        home = HomePage(
            title="Home",
            slug="test-home",
            hero_text="Welcome",
            hero_cta="Get Started",
        )
        root.add_child(instance=home)
        home.save_revision().publish()

        # Test: Check the page renders
        response = self.client.get(home.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/home_page.html")
