"""
Load demo data for the People app.
Usage:
    python manage.py load_people
    python manage.py load_people --images-only
"""

from django.core.management.base import BaseCommand
from wagtail.models import Page
from wagtail.images.models import Image


DEMO_PEOPLE = [
    {
        "first_name": "Tom",
        "last_name": "Dyson",
        "role": "Co-founder & Developer",
        "introduction": "One of the original creators of Wagtail CMS.",
        "location": "Bristol, UK",
        "team": "leadership",
        "github": "tomdyson",
        "bio": "<p>Tom is one of the co-founders of Wagtail and has been instrumental in its development.</p>",
    },
    {
        "first_name": "Matt",
        "last_name": "Westcott",
        "role": "Core Developer",
        "introduction": "Long-time Wagtail core team member and StreamField architect.",
        "location": "Oxford, UK",
        "team": "engineering",
        "github": "gasman",
        "bio": "<p>Matt is a long-time core contributor to Wagtail.</p>",
    },
    {
        "first_name": "Thibaud",
        "last_name": "Colas",
        "role": "Accessibility Lead",
        "introduction": "Focused on accessibility and front-end development.",
        "location": "Wellington, New Zealand",
        "team": "engineering",
        "github": "thibaudcolas",
        "twitter": "thibaud_colas",
        "bio": "<p>Thibaud works to ensure that Wagtail is usable by everyone.</p>",
    },
]

IMAGE_MAPPING = {
    "Tom Dyson": "lightnin_hopkins.jpg",
    "Matt Westcott": "cable-page.jpg",
    "Thibaud Colas": "francis-wolff.jpg",
}

PEOPLE_INDEX_INTRO = """
Meet the amazing people who contribute to Wagtail CMS.
"""


class Command(BaseCommand):
    help = "Load People app demo data and images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--images-only",
            action="store_true",
            help="Only add images to existing person pages",
        )

    def get_or_assign_image(self, first_name, last_name):
        """Find an existing image from IMAGE_MAPPING or fallback to first available."""
        full_name = f"{first_name} {last_name}"
        image_name = IMAGE_MAPPING.get(full_name)
        if not image_name:
            return Image.objects.first()

        existing = (
            Image.objects.filter(file__icontains=image_name.split(".")[0]).first()
            or Image.objects.filter(title__icontains=image_name.split(".")[0]).first()
        )
        return existing or Image.objects.first()

    def add_images_only(self):
        from bakerydemo.people.models import PersonPage

        people = PersonPage.objects.filter(profile_picture__isnull=True)
        updated = 0
        for person in people:
            profile_image = self.get_or_assign_image(person.first_name, person.last_name)
            if profile_image:
                person.profile_picture = profile_image
                person.save_revision().publish()
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Added images to {updated} people."))

    def handle(self, *args, **options):
        if options["images_only"]:
            self.add_images_only()
            return

        from bakerydemo.people.models import PeopleIndexPage, PersonPage

        # Find the Home page as parent
        home_page = Page.objects.filter(depth=2).first()
        if not home_page:
            self.stdout.write(self.style.ERROR("No home page found."))
            return

        # Create People Index if not exists
        people_index = PeopleIndexPage.objects.first()
        if not people_index:
            people_index = PeopleIndexPage(
                title="Our Team",
                slug="team",
                introduction=PEOPLE_INDEX_INTRO,
                show_in_menus=True,  # 👈 ensures it shows in navigation
            )
            home_page.add_child(instance=people_index)
            people_index.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("Created People Index page."))

        # Create individual Person pages
        created = 0
        for person_data in DEMO_PEOPLE:
            slug = f"{person_data['first_name']}-{person_data['last_name']}".lower()
            if PersonPage.objects.filter(slug=slug).exists():
                continue

            person_page = PersonPage(
                title=f"{person_data['first_name']} {person_data['last_name']}",
                slug=slug,
                first_name=person_data["first_name"],
                last_name=person_data["last_name"],
                role=person_data["role"],
                introduction=person_data["introduction"],
                location=person_data.get("location", ""),
                team=person_data.get("team", ""),
                github=person_data.get("github", ""),
                twitter=person_data.get("twitter", ""),
            )

            # ✅ Set StreamField content
            if "bio" in person_data:
                person_page.body = [("paragraph", person_data["bio"])]

            # Assign image if available
            image = self.get_or_assign_image(person_data["first_name"], person_data["last_name"])
            if image:
                person_page.profile_picture = image

            people_index.add_child(instance=person_page)
            person_page.save_revision().publish()
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} people successfully."))
