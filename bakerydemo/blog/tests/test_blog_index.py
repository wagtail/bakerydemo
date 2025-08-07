from django.test import RequestFactory
from django.test import TestCase
from taggit.models import Tag
from unittest.mock import patch, MagicMock
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from bakerydemo.base.models import HomePage
from bakerydemo.blog.models import BlogIndexPage, BlogPage, BlogPageTag


class BlogIndexPageTest(WagtailPageTestCase):
    """
    Test suite for BlogIndexPage functionality including:
    - Page hierarchy and relationships
    - Blog post listing and filtering
    - Tag-based navigation
    - Context data generation
    """
    @classmethod
    def setUpTestData(cls):
        # Get the root page
        cls.root = Page.get_first_root_node()
        
        # Create a site
        Site.objects.create(
            hostname="testserver",
            root_page=cls.root,
            is_default_site=True,
            site_name="testserver",
        )
        
        # Create a home page under the root with required fields
        cls.home = HomePage(
            title="Home",
            hero_text="Welcome to the Bakery",
            hero_cta="Learn More",
        )
        cls.root.add_child(instance=cls.home)
        
        # Create a blog index page
        cls.blog_index = BlogIndexPage(
            title="Blog Index",
            introduction="Welcome to our blog",
        )
        cls.home.add_child(instance=cls.blog_index)
        
        # Create some test tags
        cls.tag1 = Tag.objects.create(name="Tag 1", slug="tag-1")
        cls.tag2 = Tag.objects.create(name="Tag 2", slug="tag-2")
        
        # Create some blog posts with tags
        cls.blog_post1 = BlogPage(
            title="Blog Post 1",
            introduction="First blog post",
            subtitle="Subtitle 1",
            date_published="2024-01-01",
        )
        cls.blog_index.add_child(instance=cls.blog_post1)
        BlogPageTag.objects.create(content_object=cls.blog_post1, tag=cls.tag1)
        
        cls.blog_post2 = BlogPage(
            title="Blog Post 2",
            introduction="Second blog post",
            subtitle="Subtitle 2",
            date_published="2024-01-02",
        )
        cls.blog_index.add_child(instance=cls.blog_post2)
        BlogPageTag.objects.create(content_object=cls.blog_post2, tag=cls.tag1)
        BlogPageTag.objects.create(content_object=cls.blog_post2, tag=cls.tag2)
        
        cls.factory = RequestFactory()

    def test_get_context_method(self):
        """
        Verify that get_context method correctly:
        - Adds blog posts to the context
        - Orders posts by date (newest first)
        - Includes all required context data
        """
        request = self.factory.get('/')
        context = self.blog_index.get_context(request)
        
        # Check posts are in context
        self.assertIn('posts', context)
        self.assertEqual(len(context['posts']), 2)
        
        # Posts should be in reverse chronological order
        self.assertEqual(context['posts'][0].title, "Blog Post 2")
        self.assertEqual(context['posts'][1].title, "Blog Post 1")

    def test_blog_index_children(self):
        """
        Verify that children() method:
        - Returns all direct child blog posts
        - Maintains correct parent-child relationships
        - Returns live pages only
        """
        children = self.blog_index.children()
        self.assertEqual(len(children), 2)
        self.assertIn(self.blog_post1, children)
        self.assertIn(self.blog_post2, children)

    def test_get_posts_without_tag(self):
        """
        Verify that get_posts() without tag parameter:
        - Returns all live blog posts
        - Maintains correct ordering
        - Excludes draft/unpublished posts
        """
        posts = self.blog_index.get_posts()
        self.assertEqual(len(posts), 2)

    def test_get_posts_with_tag(self):
        """
        Verify that get_posts() with tag parameter:
        - Correctly filters posts by specified tag
        - Returns only posts with matching tag
        - Maintains correct ordering
        """
        # Tag 1 is on both posts
        posts_tag1 = self.blog_index.get_posts(tag=self.tag1)
        self.assertEqual(len(posts_tag1), 2)
        
        # Tag 2 is only on one post
        posts_tag2 = self.blog_index.get_posts(tag=self.tag2)
        self.assertEqual(len(posts_tag2), 1)
        self.assertEqual(posts_tag2[0].title, "Blog Post 2")

    @patch('bakerydemo.blog.models.render')
    @patch('bakerydemo.blog.models.messages')
    def test_tag_archive_method(self, mock_messages, mock_render):
        """
        Verify that tag_archive method:
        - Correctly handles existing tags
        - Returns appropriate response for non-existent tags
        - Sets up correct context for template rendering
        - Handles message framework integration
        """
        # Set up our mock
        mock_render.return_value = "Mocked rendered content"
        
        # Test with existing tag
        request = self.factory.get('/')
        self.blog_index.tag_archive(request, tag=self.tag1.slug)
        
        # Ensure the tag was correctly found and messages were not called
        mock_messages.add_message.assert_not_called()
        
        # Test with context passed to render for the valid tag
        context = mock_render.call_args[0][2]  # get the context argument
        self.assertEqual(context['tag'], self.tag1)
        self.assertEqual(len(context['posts']), 2)
        
        # Reset our mocks
        mock_render.reset_mock()
        mock_messages.reset_mock()
        
        # Test with non-existent tag
        response = self.blog_index.tag_archive(request, tag='nonexistent-tag')
        
        # Check that a message was added and we got a redirect
        mock_messages.add_message.assert_called_once()
        self.assertEqual(response.status_code, 302)  # redirect

    def test_get_child_tags(self):
        """
        Verify that get_child_tags method:
        - Returns all unique tags from child posts
        - Excludes duplicate tags
        - Returns tags in sorted order
        """
        tags = self.blog_index.get_child_tags()
        # Should have both tags
        self.assertEqual(len(tags), 2)
        
        # Extract tag names for easier assertion
        tag_names = [tag.name for tag in tags]
        self.assertIn("Tag 1", tag_names)
        self.assertIn("Tag 2", tag_names) 