from django.contrib.auth.models import User
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from bakerydemo.people.models import PersonIndexPage, PersonPage


class PersonIndexPageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root = Page.get_first_root_node()

        cls.site, _ = Site.objects.update_or_create(
            hostname="testserver",
            defaults={
                "root_page": cls.root,
                "is_default_site": True,
            },
        )

        cls.index_page = PersonIndexPage(
            title="People",
            slug="people",
            intro="<p>Meet our team</p>",
        )
        cls.root.add_child(instance=cls.index_page)
        cls.index_page.save_revision().publish()

        cls.person_page = PersonPage(
            title="Jane Doe",
            slug="jane-doe",
            first_name="Jane",
            last_name="Doe",
            role="Head Baker",
            department="Kitchen",
            bio="<p>Experienced artisan baker.</p>",
        )
        cls.index_page.add_child(instance=cls.person_page)
        cls.person_page.save_revision().publish()

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username="testadmin", email="test@example.com", password="password"
        )
        self.client.login(username="testadmin", password="password")

    def test_person_index_page_renders(self):
        response = self.client.get(self.index_page.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_index_page.html")
        self.assertContains(response, "Meet our team")


class PersonPageRenderTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root = Page.get_first_root_node()

        cls.site, _ = Site.objects.update_or_create(
            hostname="testserver",
            defaults={
                "root_page": cls.root,
                "is_default_site": True,
            },
        )

        cls.index_page = PersonIndexPage(
            title="People Detail",
            slug="people-detail",
        )
        cls.root.add_child(instance=cls.index_page)
        cls.index_page.save_revision().publish()

        cls.person_page = PersonPage(
            title="John Smith",
            slug="john-smith",
            first_name="John",
            last_name="Smith",
            role="Pastry Chef",
            department="Pastry",
            bio="<p>Creates delicious pastries.</p>",
        )
        cls.index_page.add_child(instance=cls.person_page)
        cls.person_page.save_revision().publish()

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username="testadmin2", email="test2@example.com", password="password"
        )
        self.client.login(username="testadmin2", password="password")

    def test_person_page_renders(self):
        response = self.client.get(self.person_page.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_page.html")
        self.assertContains(response, "John Smith")
        self.assertContains(response, "Pastry Chef")

