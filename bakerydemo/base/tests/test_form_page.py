from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from bakerydemo.base.models import FormPage


class FormPageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root = Page.get_first_root_node()

        cls.site = Site.objects.create(
            hostname="testserver",
            root_page=cls.root,
            is_default_site=True,
        )

        cls.form_page_with_introduction = FormPage(
            title="Contact us",
            slug="contact-us",
            introduction="Get in touch with our team.",
        )
        cls.root.add_child(instance=cls.form_page_with_introduction)
        cls.form_page_with_introduction.save_revision().publish()

        cls.form_page_without_introduction = FormPage(
            title="Contact us plain",
            slug="contact-us-plain",
        )
        cls.root.add_child(instance=cls.form_page_without_introduction)
        cls.form_page_without_introduction.save_revision().publish()

    def test_introduction_renders_when_set(self):
        response = self.client.get(self.form_page_with_introduction.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Get in touch with our team.")

    def test_introduction_omitted_when_blank(self):
        response = self.client.get(self.form_page_without_introduction.url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'class="intro"')
