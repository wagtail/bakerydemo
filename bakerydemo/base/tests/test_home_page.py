from django.contrib.auth.models import User
from django.test import override_settings
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase
from wagtail.test.utils.form_data import nested_form_data

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
    Tests that the HomePage
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create the page tree and site once for all tests in this class.

        This runs ONCE before all tests, not before each test.
        Both tests will share this setup, making tests faster.
        """
        # Get root page
        cls.root = Page.get_first_root_node()

        # Create site
        cls.site = Site.objects.create(
            hostname="testserver",
            root_page=cls.root,
            is_default_site=True,
        )

        # Create and publish a HomePage for the render test
        cls.home = HomePage(
            title="Home",
            slug="test-home",
            hero_text="Welcome to our site",
            hero_cta="Get Started",
        )
        cls.root.add_child(instance=cls.home)
        cls.home.save_revision().publish()

    def setUp(self):
        super().setUp()
        # Create and log in a superuser for each test
        self.user = User.objects.create_superuser(
            username="testadmin", email="test@example.com", password="password"
        )
        self.client.login(username="testadmin", password="password")

    def test_homepage_renders(self):
        """
        Test that a published HomePage created renders correctly
        """

        # Make request to the page created in setUpTestData()
        response = self.client.get(self.home.url)

        # Verify HTTP response
        self.assertEqual(response.status_code, 200)

        # Verify correct template
        self.assertTemplateUsed(response, "base/home_page.html")

        # Verify content appears on the page
        self.assertContains(response, "Welcome to our site")
        self.assertContains(response, "Get Started")

        # Alternative: Use Wagtail's built-in assertion
        self.assertPageIsRoutable(self.home)

    def test_can_create_another_homepage(self):
        """
        Test that a another Page  can be created under the root page.
        This test uses assertCanCreate()
        """

        # Create and publish the HomePage
        home_page_data = nested_form_data(
            {
                "title": "Home",
                "slug": "test-home-2",
                "hero_text": "Welcome",
                "hero_cta": "Get Started",
                "body-count": "0",
            }
        )

        self.assertCanCreate(self.root, HomePage, home_page_data)
