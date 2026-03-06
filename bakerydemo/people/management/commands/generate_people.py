from django.core.management.base import BaseCommand
from faker import Faker
from bakerydemo.people.models import PersonIndexPage, PersonPage

fake = Faker()

DEPARTMENTS = [
    "Engineering", "Design", "Marketing",
    "Research", "Operations", "Communications"
]

ROLES = [
    "Senior Engineer", "Product Designer", "Research Lead",
    "Communications Manager", "Operations Director", "UX Researcher",
    "Software Engineer", "Data Scientist", "Project Manager",
    "Content Strategist"
]

class Command(BaseCommand):
    help = "Generate fake people pages for demo"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of people pages to generate'
        )

    def handle(self, *args, **options):
        index = PersonIndexPage.objects.first()
        if not index:
            self.stdout.write(self.style.ERROR(
                'No PersonIndexPage found. '
                'Create one in the admin first.'
            ))
            return

        count = options['count']
        for i in range(count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            person = PersonPage(
                title=f"{first_name} {last_name}",
                first_name=first_name,
                last_name=last_name,
                role=fake.random_element(ROLES),
                department=fake.random_element(DEPARTMENTS),
                bio=fake.paragraph(nb_sentences=5),
                email=fake.company_email(),
                slug=fake.unique.slug(),
            )
            index.add_child(instance=person)
            person.save_revision().publish()
            self.stdout.write(f"Created: {person.title}")

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {count} people pages'
            )
        )