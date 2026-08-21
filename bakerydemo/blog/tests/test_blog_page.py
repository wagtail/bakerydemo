from django.test import override_settings
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase
from bakerydemo.blog.models import BlogIndexPage, BlogPage

@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class BlogIndexPageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        Site.objects.create(hostname="testserver", root_page=root, is_default_site=True)
        cls.index = BlogIndexPage(title="Blog", slug="blog", introduction="All our blog posts")
        root.add_child(instance=cls.index)
        cls.index.save_revision().publish()

    def test_blog_index_renders(self):
        response = self.client.get(self.index.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/blog_index_page.html")
        self.assertContains(response, "All our blog posts")


@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class BlogPageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        Site.objects.create(hostname="testserver", root_page=root, is_default_site=True)
        cls.index = BlogIndexPage(title="Blog", slug="blog")
        root.add_child(instance=cls.index)
        cls.index.save_revision().publish()
        cls.page = BlogPage(title="My First Post", slug="my-first-post", introduction="A great post")
        cls.index.add_child(instance=cls.page)
        cls.page.save_revision().publish()

    def test_blog_page_renders(self):
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/blog_page.html")
        self.assertContains(response, "My First Post")