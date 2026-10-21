from django.test import TestCase
from django.urls import reverse
from wagtail.models import Page, Site

from bakerydemo.base.models import HomePage, StandardPage
from bakerydemo.blog.models import BlogIndexPage, BlogPage


class APIV3TestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        cls.home = root.add_child(
            instance=HomePage(
                title="Home",
                slug="test-home",
                hero_text="Welcome",
                hero_cta="Find out more",
            )
        )
        Site.objects.create(
            hostname="testserver", root_page=cls.home, is_default_site=True
        )
        cls.about = cls.home.add_child(
            instance=StandardPage(title="About", slug="about", introduction="About us")
        )
        cls.blog = cls.home.add_child(
            instance=BlogIndexPage(title="Blog", slug="blog", introduction="Our blog")
        )
        # Add posts in reverse alphabetical order, so the tree order differs
        # from the ID and title orders
        cls.post_2 = cls.blog.add_child(
            instance=BlogPage(title="Second post", slug="second", introduction="Second")
        )
        cls.post_1 = cls.blog.add_child(
            instance=BlogPage(title="First post", slug="first", introduction="First")
        )
        cls.post_1.move(cls.post_2, pos="left")

        cls.home.hero_cta_link = cls.about
        cls.home.featured_section_3 = cls.blog
        cls.home.save()


class TestListingPages(APIV3TestCase):
    url = reverse("wagtailapi_v3:listing_pages")

    def test_returns_type_specific_fields(self):
        response = self.client.get(
            self.url, {"type": "blog.BlogPage", "child_of": self.blog.pk}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 2)
        item = data["items"][0]
        self.assertEqual(item["meta"]["type"], "blog.BlogPage")
        self.assertEqual(item["introduction"], "First")
        self.assertIn("image_listing", item)
        self.assertIn("parent", item["meta"])

    def test_defaults_to_tree_order(self):
        response = self.client.get(self.url, {"child_of": self.blog.pk})

        titles = [item["title"] for item in response.json()["items"]]
        self.assertEqual(titles, ["First post", "Second post"])

    def test_explicit_order(self):
        response = self.client.get(
            self.url, {"child_of": self.blog.pk, "order": "-title"}
        )

        titles = [item["title"] for item in response.json()["items"]]
        self.assertEqual(titles, ["Second post", "First post"])

    def test_multiple_types_are_specific(self):
        response = self.client.get(self.url, {"child_of": self.home.pk})

        items = {item["title"]: item for item in response.json()["items"]}
        self.assertEqual(items["About"]["meta"]["type"], "base.StandardPage")
        self.assertEqual(items["About"]["introduction"], "About us")
        self.assertEqual(items["Blog"]["meta"]["type"], "blog.BlogIndexPage")
        self.assertEqual(items["Blog"]["introduction"], "Our blog")

    def test_field_filter(self):
        response = self.client.get(
            self.url, {"type": "blog.BlogPage", "title": "Second post"}
        )

        titles = [item["title"] for item in response.json()["items"]]
        self.assertEqual(titles, ["Second post"])

    def test_pagination(self):
        response = self.client.get(
            self.url, {"child_of": self.blog.pk, "limit": 1, "offset": 1}
        )

        data = response.json()
        self.assertEqual(data["count"], 2)
        self.assertEqual([item["title"] for item in data["items"]], ["Second post"])

    def test_excludes_unpublished_pages(self):
        self.post_2.unpublish()

        response = self.client.get(self.url, {"child_of": self.blog.pk})

        titles = [item["title"] for item in response.json()["items"]]
        self.assertEqual(titles, ["First post"])


class TestPageForeignKeys(APIV3TestCase):
    def test_page_foreign_keys_are_links(self):
        response = self.client.get(
            reverse("wagtailapi_v3:detail_page", args=[self.home.pk])
        )

        data = response.json()
        link = data["hero_cta_link"]
        self.assertEqual(link["id"], self.about.pk)
        self.assertEqual(link["title"], "About")
        self.assertEqual(link["meta"]["type"], "base.StandardPage")
        self.assertEqual(link["meta"]["html_url"], "http://testserver/about/")
        self.assertEqual(data["featured_section_3"]["id"], self.blog.pk)
        self.assertIsNone(data["featured_section_1"])


class TestPreview(APIV3TestCase):
    def test_preview(self):
        self.post_1.title = "Changed title"
        preview = self.post_1.create_page_preview()

        response = self.client.get(
            reverse("wagtailapi_v3:detail_preview"),
            {"type": "blog.BlogPage", "token": preview.token},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["meta"]["type"], "blog.BlogPage")
        self.assertEqual(data["title"], "Changed title")
