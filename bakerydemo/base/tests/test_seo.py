import io

from django.core.files.images import ImageFile
from django.test import TestCase
from PIL import Image as PILImage
from wagtail.images.models import Image
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from bakerydemo.base.models import HomePage


def make_image():
    """Create a Wagtail image without needing the demo fixture."""
    file = io.BytesIO()
    PILImage.new("RGB", (1920, 900), (120, 80, 40)).save(file, format="JPEG")
    file.seek(0)
    return Image.objects.create(title="Hero", file=ImageFile(file, name="seo-hero.jpg"))


class SeoMetadataRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root = Page.get_first_root_node()
        cls.site = Site.objects.create(
            hostname="testserver",
            port=80,
            site_name="The Wagtail Bakery",
            root_page=cls.root,
            is_default_site=True,
        )
        cls.image = make_image()
        cls.home = HomePage(
            title="Home",
            slug="seo-home",
            hero_text="Welcome to our site",
            hero_cta="Get Started",
            search_description="A description for search engines.",
            image=cls.image,
        )
        cls.root.add_child(instance=cls.home)
        cls.home.save_revision().publish()

    def test_canonical_and_open_graph_tags(self):
        response = self.client.get(self.home.url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response, f'<link rel="canonical" href="{self.home.full_url}">', html=True
        )
        self.assertContains(response, '<meta property="og:type" content="website">')
        self.assertContains(
            response, f'<meta property="og:url" content="{self.home.full_url}">'
        )
        self.assertContains(response, '<meta property="og:title" content="Home">')
        self.assertContains(
            response,
            '<meta property="og:description" content="A description for search engines.">',
        )
        self.assertContains(
            response, '<meta property="og:site_name" content="The Wagtail Bakery">'
        )
        self.assertContains(response, 'property="og:image"')

    def test_no_twitter_card_tags(self):
        response = self.client.get(self.home.url)

        self.assertNotContains(response, "twitter:card")

    def test_no_open_graph_image_without_page_image(self):
        page = HomePage(
            title="No image",
            slug="seo-no-image",
            hero_text="Welcome",
            hero_cta="Get Started",
        )
        self.root.add_child(instance=page)
        page.save_revision().publish()

        response = self.client.get(page.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rel="canonical"')
        self.assertNotContains(response, 'property="og:image"')

    def test_meta_description_has_no_fallback(self):
        page = HomePage(
            title="No description",
            slug="seo-no-description",
            hero_text="Welcome",
            hero_cta="Get Started",
        )
        self.root.add_child(instance=page)
        page.save_revision().publish()

        response = self.client.get(page.url)

        self.assertContains(response, '<meta name="description" content="">')


class RobotsTxtTest(TestCase):
    def test_robots_txt_is_served(self):
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Content-Type"], 'text/plain; charset="utf-8"'
        )

        body = b"".join(response.streaming_content).decode()
        self.assertIn("User-Agent: *", body)
        self.assertIn("Disallow: /search/", body)
        self.assertNotIn("Sitemap:", body)
