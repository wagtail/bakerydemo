"""
Complete People App Demo Content and Management
Single file containing all data and functionality

Usage:
    python manage.py load_people           # Load demo data with images
    python manage.py load_people --images-only  # Just add images to existing people
"""

from django.core.management.base import BaseCommand
from wagtail.models import Page
from wagtail.images.models import Image


# ============================================================================
# DEMO DATA
# ============================================================================

DEMO_PEOPLE = [
    {
        "first_name": "Tom",
        "last_name": "Dyson",
        "role": "Co-founder & Developer",
        "introduction": "One of the original creators of Wagtail CMS. Passionate about building elegant content management solutions.",
        "location": "Bristol, UK",
        "team": "leadership",
        "github": "tomdyson",
        "bio": "<p>Tom is one of the co-founders of Wagtail and has been instrumental in its development since the beginning. He's passionate about creating tools that help content creators and developers work together more effectively.</p><p>With years of experience in web development, Tom focuses on making Wagtail accessible, powerful, and enjoyable to use.</p>"
    },
    {
        "first_name": "Matt",
        "last_name": "Westcott",
        "role": "Core Developer",
        "introduction": "Long-time Wagtail core team member, maintainer, and StreamField architect.",
        "location": "Oxford, UK",
        "team": "engineering",
        "github": "gasman",
        "bio": "<p>Matt has been a core contributor to Wagtail for many years and is responsible for many of its most powerful features, including significant work on StreamField.</p><p>His deep understanding of Django and commitment to code quality have helped shape Wagtail into the robust CMS it is today.</p>"
    },
    {
        "first_name": "Thibaud",
        "last_name": "Colas",
        "role": "Accessibility Lead",
        "introduction": "Wagtail core team member focused on accessibility, front-end development, and developer experience.",
        "location": "Wellington, New Zealand",
        "team": "engineering",
        "github": "thibaudcolas",
        "twitter": "thibaud_colas",
        "bio": "<p>Thibaud is a core team member who champions accessibility in Wagtail. He works to ensure that Wagtail is usable by everyone, regardless of their abilities.</p><p>He's also deeply involved in improving the developer experience and modernizing Wagtail's front-end architecture.</p>"
    },
    {
        "first_name": "Storm",
        "last_name": "Heg",
        "role": "Core Contributor",
        "introduction": "Active Wagtail contributor focusing on improving the CMS experience and developer tools.",
        "location": "Netherlands",
        "team": "engineering",
        "github": "Stormheg",
        "bio": "<p>Storm is an active contributor to Wagtail who focuses on improving both the editor experience and developer workflows.</p><p>His contributions span across various areas of the CMS, always with an eye toward making things more intuitive and efficient.</p>"
    },
    {
        "first_name": "LB",
        "last_name": "Johnston",
        "role": "Community Manager",
        "introduction": "Wagtail community advocate, documentation enthusiast, and event organizer.",
        "location": "Melbourne, Australia",
        "team": "community",
        "github": "lb-",
        "twitter": "lbj_online",
        "bio": "<p>LB is passionate about building inclusive open-source communities and helping people get started with Wagtail.</p><p>From organizing community events to improving documentation, LB works to make Wagtail welcoming to newcomers and veterans alike.</p>"
    },
    {
        "first_name": "Sage",
        "last_name": "Abdullah",
        "role": "Core Developer",
        "introduction": "Wagtail core team member working on internals, APIs, and developer experience.",
        "location": "Jakarta, Indonesia",
        "team": "engineering",
        "github": "laymonage",
        "twitter": "laymonage",
        "bio": "<p>Sage is a core team member who contributes across many areas of Wagtail, with particular focus on the API and internal architecture.</p><p>His work helps ensure Wagtail stays modern, maintainable, and powerful for developers building with it.</p>"
    },
]

# Map person names to existing demo images from bakerydemo (if load_initial_data was run)
IMAGE_MAPPING = {
    'Tom Dyson': 'lightnin_hopkins.jpg',
    'Matt Westcott': 'cable-page.jpg',
    'Thibaud Colas': 'francis-wolff.jpg',
    'Storm Heg': 'chris-albertson.jpg',
    'LB Johnston': 'nat-hentoff.jpg',
    'Sage Abdullah': 'ira-gitler.jpg',
}

PEOPLE_INDEX_INTRO = """
Meet the amazing people who contribute to Wagtail CMS. This open-source project
thrives because of the dedication and expertise of developers, designers, and
community members from around the world.

Whether they're writing code, improving documentation, organizing events, or
helping others in the community, each person plays a vital role in making
Wagtail the powerful and friendly CMS it is today.
"""


# ============================================================================
# MANAGEMENT COMMAND
# ============================================================================

class Command(BaseCommand):
    help = 'Setup People app with demo data and images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--images-only',
            action='store_true',
            help='Only add images to existing person pages',
        )

    def get_or_assign_image(self, first_name, last_name):
        """Get an existing image from the database to use as profile picture"""
        full_name = f"{first_name} {last_name}"

        # Check if there's a mapped image for this person
        if full_name in IMAGE_MAPPING:
            image_name = IMAGE_MAPPING[full_name]

            # Try exact match on filename
            existing = Image.objects.filter(file__icontains=image_name.split('.')[0]).first()
            if existing:
                self.stdout.write(f"      ✓ Using existing image: {existing.title}")
                return existing

            # Try to find by title
            title_search = image_name.split('.')[0].replace('_', ' ').replace('-', ' ')
            existing = Image.objects.filter(title__icontains=title_search).first()
            if existing:
                self.stdout.write(f"      ✓ Using existing image: {existing.title}")
                return existing

        # If no specific mapping, try to get any available image
        any_image = Image.objects.first()
        if any_image:
            self.stdout.write(f"      ℹ Using random image: {any_image.title}")
            return any_image

        self.stdout.write(f"      ⚠ No images available in database")
        return None

    def add_images_only(self):
        """Add images to existing person pages"""
        from bakerydemo.people.models import PersonPage

        self.stdout.write("=" * 60)
        self.stdout.write("ADDING PROFILE IMAGES TO PERSON PAGES")
        self.stdout.write("=" * 60)

        # Check if any images exist in the database
        total_images = Image.objects.count()
        if total_images == 0:
            self.stdout.write(self.style.WARNING("\n⚠ No images found in database!"))
            self.stdout.write("Please run: python manage.py load_initial_data")
            self.stdout.write("This will load the bakerydemo images that can be used as profile pictures.\n")
            return

        self.stdout.write(f"\nFound {total_images} images in database")

        people_without_images = PersonPage.objects.filter(profile_picture__isnull=True)
        total = people_without_images.count()

        if total == 0:
            self.stdout.write(self.style.SUCCESS("\n✓ All person pages already have profile images!"))
            return

        self.stdout.write(f"Found {total} person page(s) without profile images\n")

        success_count = 0
        for person in people_without_images:
            self.stdout.write(f"Processing: {person.first_name} {person.last_name}")

            # Get an existing image from the database
            profile_image = self.get_or_assign_image(person.first_name, person.last_name)

            if profile_image:
                person.profile_picture = profile_image
                person.save_revision().publish()
                self.stdout.write(self.style.SUCCESS(f"   ✓ Added profile image to {person.full_name}"))
                success_count += 1

        self.stdout.write(f"\n✓ Added images to {success_count} person page(s)!")

    def handle(self, *args, **options):
        if options['images_only']:
            self.add_images_only()
            return

        # Full setup
        from bakerydemo.people.models import PeopleIndexPage, PersonPage

        self.stdout.write("=" * 60)
        self.stdout.write("SETTING UP PEOPLE APP WITH DEMO DATA")
        self.stdout.write("=" * 60)

        # Find home page
        try:
            from bakerydemo.base.models import HomePage
            home_page = HomePage.objects.first()
            if not home_page:
                home_page = Page.objects.filter(depth=2).first()
        except:
            home_page = Page.objects.filter(depth=2).first()

        if not home_page:
            self.stdout.write(self.style.ERROR("Could not find a home page."))
            return

        self.stdout.write(f"\nUsing '{home_page.title}' as parent page")

        # Check if People Index Page exists
        people_index = PeopleIndexPage.objects.first()

        if people_index:
            self.stdout.write(self.style.WARNING(f"\nPeople Index Page exists: '{people_index.title}'"))
            # Ensure the people index appears in site menus
            try:
                if not people_index.show_in_menus:
                    people_index.show_in_menus = True
                    people_index.save_revision().publish()
                    self.stdout.write(self.style.SUCCESS(f"   ✓ Enabled 'show_in_menus' for: '{people_index.title}'"))
            except Exception:
                # non-fatal: if the page doesn't have the attribute or save fails, continue
                pass
            use_existing = input("Use existing page? (y/n): ").lower() == 'y'
            if not use_existing:
                return
        else:
            self.stdout.write("\n1. Creating People Index Page...")
            people_index = PeopleIndexPage(
                title="Our Team",
                slug="team",
                show_in_menus=True,
                introduction=PEOPLE_INDEX_INTRO,
            )
            home_page.add_child(instance=people_index)
            people_index.save_revision().publish()
            self.stdout.write(self.style.SUCCESS(f"   ✓ Created: '{people_index.title}' at /{people_index.slug}/"))

        # Create Person Pages
        self.stdout.write("\n2. Creating Person Pages...")
        created_count = 0
        skipped_count = 0

        for person_data in DEMO_PEOPLE:
            slug = f"{person_data['first_name']}-{person_data['last_name']}".lower()

            if PersonPage.objects.filter(slug=slug).exists():
                self.stdout.write(f"   - Skipped: {person_data['first_name']} {person_data['last_name']} (exists)")
                skipped_count += 1
                continue

            self.stdout.write(f"\n   Creating: {person_data['first_name']} {person_data['last_name']}")

            person_page = PersonPage(
                title=f"{person_data['first_name']} {person_data['last_name']}",
                slug=slug,
                first_name=person_data['first_name'],
                last_name=person_data['last_name'],
                role=person_data['role'],
                introduction=person_data['introduction'],
                location=person_data.get('location', ''),
                team=person_data.get('team', ''),
                github=person_data.get('github', ''),
                twitter=person_data.get('twitter', ''),
                email=person_data.get('email', ''),
                website=person_data.get('website', ''),
                linkedin=person_data.get('linkedin', ''),
            )

            if 'bio' in person_data:
                person_page.body = [('paragraph', person_data['bio'])]

            # Assign an existing image as profile picture
            profile_image = self.get_or_assign_image(person_data['first_name'], person_data['last_name'])
            if profile_image:
                person_page.profile_picture = profile_image

            people_index.add_child(instance=person_page)
            person_page.save_revision().publish()

            self.stdout.write(self.style.SUCCESS(f"      ✓ Created {person_data['first_name']} {person_data['last_name']}"))
            created_count += 1

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("SETUP COMPLETE!"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"\nSummary:")
        self.stdout.write(f"  People Index: {people_index.url}")
        self.stdout.write(f"  Created: {created_count}")
        self.stdout.write(f"  Skipped: {skipped_count}")
        self.stdout.write("\n✓ Visit the team page to see the results!\n")
