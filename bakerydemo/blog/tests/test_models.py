from django.test import TestCase
from wagtail.models import Page, Site
from wagtail.rich_text import RichText
from wagtail.test.utils import WagtailPageTestCase

from bakerydemo.base.models import HomePage
from bakerydemo.blog.models import BlogIndexPage, BlogPage


class BlogPageTest(WagtailPageTestCase):
    """
    Test the BlogPage model and its fields
    """
    @classmethod
    def setUpTestData(cls):
        # Get the root page
        root = Page.get_first_root_node()
        
        # Create a site
        Site.objects.create(
            hostname="testserver",
            root_page=root,
            is_default_site=True,
            site_name="testserver",
        )
        
        # Create a home page under the root with required fields
        home = HomePage(
            title="Home",
            hero_text="Welcome to the Bakery",
            hero_cta="Learn More",
        )
        root.add_child(instance=home)
        
        # Create a blog index page
        blog_index = BlogIndexPage(
            title="Blog Index",
            introduction="Introduction to the blog",
        )
        home.add_child(instance=blog_index)
        
        # Create a test blog page
        cls.blog_page = BlogPage(
            title="Test Blog Page",
            introduction="Test blog page introduction",
            subtitle="Test Subtitle",
            date_published="2024-01-01",
        )
        blog_index.add_child(instance=cls.blog_page)
        
        # Add StreamField content
        cls.blog_page.body.append(('heading_block', {
            'heading_text': 'Test Heading',
            'size': 'h2'
        }))
        cls.blog_page.body.append(('paragraph_block', RichText(
            '<p>This is a test paragraph with <b>bold text</b>.</p>'
        )))
        cls.blog_page.save()

    def test_blog_page_content(self):
        """Test that the blog page content is correctly saved and rendered"""
        # Get the page
        page = BlogPage.objects.get(title="Test Blog Page")
        
        # Check basic field values
        self.assertEqual(page.title, "Test Blog Page")
        self.assertEqual(page.introduction, "Test blog page introduction")
        self.assertEqual(page.subtitle, "Test Subtitle")
        self.assertEqual(str(page.date_published), "2024-01-01")
        
        # Check StreamField content
        self.assertEqual(len(page.body), 2)
        
        # Check heading block
        heading_block = page.body[0].value
        self.assertEqual(heading_block['heading_text'], 'Test Heading')
        self.assertEqual(heading_block['size'], 'h2')
        
        # Check paragraph block - convert the RichText object to a string
        paragraph_content = str(page.body[1].value)
        self.assertIn('<p>This is a test paragraph with <b>bold text</b>.</p>', paragraph_content)

    def test_blog_page_parent_page_types(self):
        """Test that BlogPage can only be created under BlogIndexPage"""
        self.assertAllowedParentPageTypes(
            BlogPage, {BlogIndexPage}
        )

    def test_blog_page_subpage_types(self):
        """Test that BlogPage doesn't allow any subpages"""
        self.assertAllowedSubpageTypes(
            BlogPage, {}
        )
        
    def test_blog_page_url_path(self):
        """Test that the page URL path is generated correctly"""
        page = BlogPage.objects.get(title="Test Blog Page")
        self.assertIn('test-blog-page', page.url_path)
        self.assertIn('blog-index', page.url_path) 