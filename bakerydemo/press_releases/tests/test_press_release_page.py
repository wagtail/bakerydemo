from django.contrib.auth.models import User
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from bakerydemo.press_releases.models import PressReleaseIndexPage, PressReleasePage


class PressReleaseIndexPageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root = Page.get_first_root_node()

        cls.site, _ = Site.objects.update_or_create(
            hostname="testserver",
            defaults={
                "root_page": cls.root,
                "is_default_site": True,
            },
        )

        cls.index_page = PressReleaseIndexPage(
            title="Press Releases",
            slug="press-releases-test",
            intro="<p>Latest news</p>",
        )
        cls.root.add_child(instance=cls.index_page)
        cls.index_page.save_revision().publish()

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username="testadmin", email="test@example.com", password="password"
        )
        self.client.login(username="testadmin", password="password")

    def test_press_release_index_page_renders(self):
        response = self.client.get(self.index_page.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "press_releases/press_release_index_page.html")
        self.assertContains(response, "Latest news")


class PressReleasePageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root = Page.get_first_root_node()

        cls.site, _ = Site.objects.update_or_create(
            hostname="testserver",
            defaults={
                "root_page": cls.root,
                "is_default_site": True,
            },
        )

        cls.index_page = PressReleaseIndexPage(
            title="Press Releases Detail",
            slug="press-releases-detail-test",
        )
        cls.root.add_child(instance=cls.index_page)
        cls.index_page.save_revision().publish()

        cls.press_release_page = PressReleasePage(
            title="Bakery Opens New Location",
            slug="bakery-opens-new-location",
            date="2026-01-15",
            intro="The bakery is expanding.",
            body="<p>We are excited to announce a new location.</p>",
            source="PR Newswire",
            contact_email="press@example.com",
        )
        cls.index_page.add_child(instance=cls.press_release_page)
        cls.press_release_page.save_revision().publish()

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username="testadmin2", email="test2@example.com", password="password"
        )
        self.client.login(username="testadmin2", password="password")

    def test_press_release_page_renders(self):
        response = self.client.get(self.press_release_page.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "press_releases/press_release_page.html")
        self.assertContains(response, "Bakery Opens New Location")
        self.assertContains(response, "PR Newswire")
