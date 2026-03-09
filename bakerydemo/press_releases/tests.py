from wagtail.test.utils import WagtailPageTestCase
from wagtail.models import Page
from bakerydemo.press_releases.models import PressReleaseIndexPage, PressReleasePage
import datetime


class PressReleaseIndexPageTest(WagtailPageTestCase):
    def setUp(self):
        root = Page.objects.first()
        self.index = PressReleaseIndexPage(
            title="Press Releases",
            slug="press-releases",
        )
        root.add_child(instance=self.index)
        self.index.save_revision().publish()

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
    def setUp(self):
        root = Page.objects.first()
        self.index = PressReleaseIndexPage(
            title="Press Releases",
            slug="press-releases",
        )
        root.add_child(instance=self.index)
        self.index.save_revision().publish()

        self.release = PressReleasePage(
            title="Bakery Wins Award",
            slug="bakery-wins-award",
            date=datetime.date.today(),
            intro="We are thrilled to announce...",
            body="<p>Full details here.</p>",
            source="Bakery News",
        )
        self.index.add_child(instance=self.release)
        self.release.save_revision().publish()

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
