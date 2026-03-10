from django.core.management.base import BaseCommand
from faker import Faker
from bakerydemo.press_releases.models import PressReleaseIndexPage, PressReleasePage

fake = Faker()

SOURCES = [
    "Reuters", "Associated Press", "PR Newswire",
    "Business Wire", "Globe Newswire", "PR Web"
]

class Command(BaseCommand):
    help = "Generate fake press release pages for demo"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of press release pages to generate'
        )

    def handle(self, *args, **options):
        index = PressReleaseIndexPage.objects.first()
        if not index:
            self.stdout.write(self.style.ERROR(
                'No PressReleaseIndexPage found. '
                'Create one in the admin first.'
            ))
            return

        count = options['count']
        for i in range(count):
            title = fake.sentence(nb_words=6).rstrip('.')
            release = PressReleasePage(
                title=title,
                date=fake.date_between(start_date='-2y', end_date='today'),
                intro=fake.paragraph(nb_sentences=2),
                body=f"<p>{fake.paragraph(nb_sentences=5)}</p>",
                source=fake.random_element(SOURCES),
                contact_email=fake.company_email(),
                slug=fake.unique.slug(),
            )
            index.add_child(instance=release)
            release.save_revision().publish()
            self.stdout.write(f"Created: {release.title}")

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {count} press release pages'
        ))