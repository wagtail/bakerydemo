from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from bakerydemo.breads.models import BreadPage


class BreadPageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create the page tree and site once for all tests in this class.

        Steps:
        1. Identify the root page.
        2. Create a Site pointing at the root.
        3. Create a BreadPage instance with the required fields.
        4. Add it to the tree and publish so it is live.
        """
        # 1. Identify the root page
        cls.root = Page.get_first_root_node()

        # 2. Create the Site that will serve our test pages
        cls.site = Site.objects.create(
            hostname="testserver",
            root_page=cls.root,
            is_default_site=True,
        )

        # 3. Create the BreadPage instance we want to test
        cls.bread_page = BreadPage(
            title="Test bread",
            slug="test-bread",
            introduction="A test bread page.",
        )

        # 4. Add to the tree and publish so it is live
        cls.root.add_child(instance=cls.bread_page)
        cls.bread_page.save_revision().publish()

    def test_bread_page_renders(self):
        response = self.client.get(self.bread_page.url)
        self.assertEqual(response.status_code, 200)

