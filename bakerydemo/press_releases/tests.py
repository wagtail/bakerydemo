from django.contrib.auth.models import User
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase
from bakerydemo.press_releases.models import PressReleaseIndexPage, PressReleasePage
import datetime


class PressReleaseIndexPageTest(WagtailPageTestCase):
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

        cls.index = PressReleaseIndexPage(
            title="Press Releases",
            slug="press-releases-test",
        )
        cls.root.add_child(instance=cls.index)
        cls.index.save_revision().publish()

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username="testadmin", email="test@example.com", password="password"
        )
        self.client.login(username="testadmin", password="password")

    def test_index_page_status_code(self):
        response = self.client.get(self.index.url)
        self.assertEqual(response.status_code, 200)

    def test_index_page_uses_correct_template(self):
        response = self.client.get(self.index.url)
        self.assertTemplateUsed(
            response,
            "press_releases/press_release_index_page.html"
        )


class PressReleasePageTest(WagtailPageTestCase):
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

        cls.index = PressReleaseIndexPage(
            title="Press Releases",
            slug="press-releases-page-test",
        )
        cls.root.add_child(instance=cls.index)
        cls.index.save_revision().publish()

        cls.release = PressReleasePage(
            title="Bakery Wins Award",
            slug="bakery-wins-award",
            date=datetime.date.today(),
            intro="We are thrilled to announce...",
            body="<p>Full details here.</p>",
            source="Bakery News",
        )
        cls.index.add_child(instance=cls.release)
        cls.release.save_revision().publish()

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username="testadmin2", email="test2@example.com", password="password"
        )
        self.client.login(username="testadmin2", password="password")

    def test_press_release_page_status_code(self):
        response = self.client.get(self.release.url)
        self.assertEqual(response.status_code, 200)

    def test_press_release_page_uses_correct_template(self):
        response = self.client.get(self.release.url)
        self.assertTemplateUsed(
            response,
            "press_releases/press_release_page.html"
        )

    def test_press_release_shows_title(self):
        response = self.client.get(self.release.url)
        self.assertContains(response, "Bakery Wins Award")
# Create your tests here.
