from django.test import TestCase
from django.urls import reverse

from bakerydemo.base.models import Person


class PersonAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.live_person = Person.objects.create(
            first_name="Ada",
            last_name="Lovelace",
            job_title="Programmer",
        )
        cls.draft_person = Person.objects.create(
            first_name="Grace",
            last_name="Hopper",
            job_title="Computer Scientist",
            live=False,
        )

    def test_people_list_returns_live_people(self):
        response = self.client.get(reverse("people_api"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": self.live_person.id,
                    "first_name": "Ada",
                    "last_name": "Lovelace",
                    "job_title": "Programmer",
                    "image": None,
                }
            ],
        )

    def test_person_detail_returns_live_person(self):
        response = self.client.get(
            reverse("person_api_detail", kwargs={"pk": self.live_person.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": self.live_person.id,
                "first_name": "Ada",
                "last_name": "Lovelace",
                "job_title": "Programmer",
                "image": None,
            },
        )

    def test_person_detail_hides_draft_people(self):
        response = self.client.get(
            reverse("person_api_detail", kwargs={"pk": self.draft_person.pk})
        )

        self.assertEqual(response.status_code, 404)
