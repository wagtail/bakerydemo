from django.test import TestCase
from wagtail.models import Site
from wagtail.test.utils import WagtailPageTests
from bakerydemo.blog.models import BlogIndexPage, BlogPage

class BlogPageTests(WagtailPageTests):
    def setUp(self):
        # Get the default site
        self.site = Site.objects.get(is_default_site=True)
        self.root = self.site.root_page
        
        # Create a BlogIndexPage
        self.blog_index = BlogIndexPage(
            title="Blog Index",
            slug="blog",
            introduction="Welcome to the blog"
        )
        self.root.add_child(instance=self.blog_index)
        self.blog_index.save_revision().publish()

        # Create some BlogPages
        self.blog_post = BlogPage(
            title="First Post",
            slug="first-post",
            introduction="Intro",
            body=[('paragraph', 'Content')],
            date_published="2023-01-01"
        )
        self.blog_index.add_child(instance=self.blog_post)
        self.blog_post.save_revision().publish()
        
        # Add a tag to the post
        self.blog_post.tags.add("bread")
        self.blog_post.save_revision().publish()

    def test_blog_index_page_renders(self):
        """Test that the blog index page renders correctly"""
        response = self.client.get(self.blog_index.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_index_page.html')
        self.assertContains(response, "First Post")

    def test_tag_filtering(self):
        """Test that filtering by tag works"""
        # Create a post without the tag
        other_post = BlogPage(
            title="Other Post",
            slug="other-post",
            introduction="Intro",
            body=[('paragraph', 'Content')],
            date_published="2023-01-02"
        )
        self.blog_index.add_child(instance=other_post)
        other_post.save_revision().publish()

        # url for tag filter
        url = self.blog_index.url + self.blog_index.reverse_subpage('tag_archive', args=('bread',))
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Should contain the tagged post
        self.assertContains(response, "First Post")
        # Should NOT contain the untagged post
        self.assertNotContains(response, "Other Post")

    def test_get_posts_method(self):
        from taggit.models import Tag
        # Directly test the get_posts method logic
        self.assertIn(self.blog_post, self.blog_index.get_posts())
        
        # Test filtering
        tag = Tag.objects.get(slug="bread")
        tagged_posts = self.blog_index.get_posts(tag=tag)
        self.assertIn(self.blog_post, tagged_posts)
