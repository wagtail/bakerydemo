from django.test import TestCase
from wagtail.models import Page

from bakerydemo.base.models import Person
from bakerydemo.blog.models import BlogIndexPage, BlogPage, BlogPersonRelationship


class BlogPersonRelationshipDuplicateTestCase(TestCase):
    """
    Regression tests for the duplicate (page, person) IntegrityError.

    When autosave or concurrent saves interact with a through model that has a
    UniqueConstraint, modelcluster can attempt to INSERT a row that already
    exists, causing an IntegrityError.
    """

    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()

        blog_index = BlogIndexPage(
            title="Blog",
            slug="blog",
            introduction="Blog index",
        )
        root.add_child(instance=blog_index)

        cls.blog_page = BlogPage(
            title="Test Blog Post",
            slug="test-blog-post",
        )
        blog_index.add_child(instance=cls.blog_page)

        cls.person = Person.objects.create(
            first_name="Test",
            last_name="Author",
            job_title="Writer",
        )

    def test_committing_cluster_with_existing_and_idless_relationship_does_not_duplicate(
        self,
    ):
        """
        When a committed (page, person) row already exists in the DB and the page
        cluster also contains an id-less entry for the same person, save() must not
        raise an IntegrityError or create a duplicate row.
        """
        existing = BlogPersonRelationship.objects.create(
            page=self.blog_page, person=self.person
        )

        # Load the page fresh — simulates a new request (e.g. autosave from another tab)
        page = BlogPage.objects.get(pk=self.blog_page.pk)

        # Add an id-less relationship, as the admin inline formset would submit
        page.blog_person_relationship.add(BlogPersonRelationship(person=self.person))

        page.save()  # must not raise IntegrityError

        relationships = BlogPersonRelationship.objects.filter(
            page=self.blog_page, person=self.person
        )
        self.assertEqual(relationships.count(), 1)
        self.assertTrue(relationships.filter(pk=existing.pk).exists())
