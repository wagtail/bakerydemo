from django.contrib.auth.models import User
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase
from wagtail.test.utils.form_data import nested_form_data, streamfield

from bakerydemo.base.models import HomePage


class HomePageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create the page tree and site once for all tests in this class.

        This runs ONCE before all tests, not before each test.
        All tests will share this setup, making tests faster.
        """
        cls.root = Page.get_first_root_node()

        cls.site = Site.objects.create(
            hostname="testserver",
            root_page=cls.root,
            is_default_site=True,
        )

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

        self.user = User.objects.create_superuser(
            username="testadmin", email="test@example.com", password="password"
        )
        self.client.login(username="testadmin", password="password")

    def test_homepage_renders(self):
        response = self.client.get(self.home.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "base/home_page.html")

        self.assertContains(response, "Welcome to our site")
        self.assertContains(response, "Get Started")

    def test_can_create_another_homepage(self):
        home_page_data = nested_form_data(
            {
                "title": "Home",
                "slug": "test-home-2",
                "hero_text": "Welcome",
                "hero_cta": "Get Started",
                "body": streamfield(
                    [
                        ("text", "This is some dummy content for the body block"),
                    ]
                ),
            }
        )

        self.assertCanCreate(self.root, HomePage, home_page_data)
