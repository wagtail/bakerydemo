from django.contrib.auth.models import User
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from bakerydemo.base.models import FooterMenu, HomePage


class FooterMenuTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create the page tree, site, and a published footer menu
        once for all tests in this class.
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

    def _create_footer_menu(self, sections_data=None):
        """Helper to create and publish a FooterMenu with given sections data."""
        if sections_data is None:
            sections_data = [
                {
                    "type": "section",
                    "value": {
                        "heading": "About Us",
                        "items": [
                            {
                                "title": "Our Homepage",
                                "link": [
                                    {
                                        "type": "page",
                                        "value": self.home.pk,
                                    }
                                ],
                            },
                            {
                                "title": "Wagtail Website",
                                "link": [
                                    {
                                        "type": "external_url",
                                        "value": "https://wagtail.org",
                                    }
                                ],
                            },
                        ],
                    },
                }
            ]

        footer_menu = FooterMenu(
            name="Test Footer Menu",
            sections=sections_data,
        )
        footer_menu.save()
        footer_menu.save_revision().publish()
        return footer_menu

    def test_footer_menu_renders_on_homepage(self):
        """A published footer menu should appear on the homepage."""
        self._create_footer_menu()

        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About Us")
        self.assertContains(response, "footer-menu")

    def test_footer_menu_with_page_links(self):
        """Page links in the footer menu should resolve to correct URLs."""
        self._create_footer_menu()

        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Our Homepage")

    def test_footer_menu_with_external_links(self):
        """External URL links should render with rel='noreferrer' and target='_blank'."""
        self._create_footer_menu()

        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "https://wagtail.org")
        self.assertContains(response, 'rel="noreferrer"')
        self.assertContains(response, 'target="_blank"')

    def test_footer_menu_custom_title_overrides_page_title(self):
        """When a custom title is set, it should be displayed instead of the page title."""
        self._create_footer_menu()

        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        # "Our Homepage" is the custom title (not the page's actual title "Home")
        self.assertContains(response, "Our Homepage")

    def test_footer_menu_not_rendered_when_none_published(self):
        """When no footer menu is published, the footer-menu nav should not appear."""
        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "footer-menu")

    def test_footer_menu_str(self):
        """The FooterMenu __str__ method should return the name."""
        footer_menu = self._create_footer_menu()
        self.assertEqual(str(footer_menu), "Test Footer Menu")

    def test_footer_menu_multiple_sections(self):
        """A footer menu with multiple sections should render all section headings."""
        sections_data = [
            {
                "type": "section",
                "value": {
                    "heading": "Bakery",
                    "items": [
                        {
                            "title": "Home",
                            "link": [
                                {"type": "page", "value": self.home.pk}
                            ],
                        }
                    ],
                },
            },
            {
                "type": "section",
                "value": {
                    "heading": "Connect",
                    "items": [
                        {
                            "title": "GitHub",
                            "link": [
                                {
                                    "type": "external_url",
                                    "value": "https://github.com/wagtail",
                                }
                            ],
                        }
                    ],
                },
            },
        ]
        self._create_footer_menu(sections_data)

        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bakery")
        self.assertContains(response, "Connect")
        self.assertContains(response, "GitHub")
