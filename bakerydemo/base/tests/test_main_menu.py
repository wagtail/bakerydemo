from django.contrib.auth.models import User
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from bakerydemo.base.models import MainMenu, HomePage


class MainMenuTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
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

    def _create_main_menu(self, items_data=None):
        if items_data is None:
            items_data = [
                {
                    "type": "item",
                    "value": {
                        "title": "Home",
                        "link": [{"type": "page", "value": self.home.pk}],
                    },
                },
                {
                    "type": "item",
                    "value": {
                        "title": "Wagtail",
                        "link": [
                            {"type": "external_url", "value": "https://wagtail.org"}
                        ],
                    },
                },
            ]

        main_menu = MainMenu(name="Test Main Menu", items=items_data)
        main_menu.save()
        main_menu.save_revision().publish()
        return main_menu

    def test_main_menu_renders_on_homepage(self):
        self._create_main_menu()
        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home")
        self.assertContains(response, "Wagtail")

    def test_main_menu_with_page_links(self):
        self._create_main_menu()
        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home")

    def test_main_menu_with_external_links(self):
        self._create_main_menu()
        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "https://wagtail.org")
        self.assertContains(response, 'rel="noreferrer"')

    def test_main_menu_not_rendered_when_none_published(self):
        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "https://wagtail.org")

    def test_main_menu_str(self):
        main_menu = self._create_main_menu()
        self.assertEqual(str(main_menu), "Test Main Menu")

    def test_main_menu_custom_title(self):
        items_data = [
            {
                "type": "item",
                "value": {
                    "title": "Our Homepage",
                    "link": [{"type": "page", "value": self.home.pk}],
                },
            },
        ]
        self._create_main_menu(items_data)
        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Our Homepage")
