import random
from datetime import date, time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import lorem_ipsum, timezone
from django.utils.text import slugify
from taggit.models import Tag
from wagtail.images.models import Image
from wagtail.models import Site
from wagtail.rich_text import RichText
from willow.image import Image as WillowImage

from bakerydemo.base.models import HomePage, Person
from bakerydemo.blog.models import BlogIndexPage, BlogPage, BlogPersonRelationship
from bakerydemo.breads.models import BreadIngredient, BreadPage, BreadsIndexPage, BreadType, Country
from bakerydemo.locations.models import LocationOperatingHours, LocationPage, LocationsIndexPage

FIXTURE_MEDIA_DIR = Path(settings.PROJECT_DIR) / "base/fixtures/media/original_images"

# Benchmark configuration constants
STREAMFIELD_BLOCKS = 100
INLINE_PANEL_ITEMS = 100
RICH_TEXT_PARAGRAPHS = 100
REVISIONS_PER_PAGE = 5

# Page count constants
BLOG_PAGES = 100
BREAD_PAGES = 100
LOCATION_PAGES = 100


class Command(BaseCommand):
    help = 'Load benchmark data for performance testing using existing content types'

    def handle(self, *args, **options):
        self.stdout.write('Starting benchmark data generation.')

        try:
            home_page = Site.objects.get(is_default_site=True).root_page
        except (Site.DoesNotExist, Site.MultipleObjectsReturned) as e:
            self.stdout.write(f'Could not find home page: {e}. Please set up the site first.')
            return

        created = self.create_blog_pages(home_page, BLOG_PAGES)
        self.stdout.write(f'Created {created} new blog pages')

        created = self.create_bread_pages(home_page, BREAD_PAGES)
        self.stdout.write(f'Created {created} new bread pages')

        created = self.create_location_pages(home_page, LOCATION_PAGES)
        self.stdout.write(f'Created {created} new location pages')

        self.stdout.write('Benchmark data generation complete!')

    def _get_images_cache(self):
        """Cache images to avoid repeated queries."""
        if not hasattr(self, '_images_cache'):
            self._images_cache = list(Image.objects.all()   )
        return self._images_cache

    def get_random_image(self):
        """Return a random image or None if no images exist."""
        images = self._get_images_cache()
        return random.choice(images) if images else None

    def _generate_paragraph(self):
        """Generate a random lorem ipsum paragraph."""
        return lorem_ipsum.paragraph()

    def _get_first_image(self):
        """Return the first available image or None."""
        images = self._get_images_cache()
        return images[0] if images else None

    def _create_heading_block(self, index):
        """Create a heading block with fixed text based on index."""
        heading_sizes = ['h2', 'h3', 'h4', '']
        heading_texts = [
            'Introduction to Baking',
            'The Art of Bread Making',
            'Essential Ingredients',
            'Traditional Techniques',
            'Modern Innovations',
        ]
        return ('heading_block', {
            'heading_text': heading_texts[index % len(heading_texts)],
            'size': heading_sizes[index % len(heading_sizes)]
        })

    def _create_paragraph_block(self, index, num_paragraphs=2):
        """Create a paragraph block with fixed paragraphs."""
        fixed_paragraphs = [
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
            'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
            'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
            'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.',
        ]
        paragraph_text = '\n'.join(fixed_paragraphs[:num_paragraphs])
        return ('paragraph_block', RichText(paragraph_text))

    def _create_image_block(self, index):
        """Create an image block with a fixed image."""
        image = self._get_first_image()
        if image:
            captions = [
                'Traditional baking methods',
                'Fresh ingredients',
                'Artisan craftsmanship',
                'Quality products',
                '',
            ]
            attributions = [
                'Photo by Baker',
                'Courtesy of Bakery',
                '',
                'Professional photography',
                '',
            ]
            return ('image_block', {
                'image': image,
                'caption': captions[index % len(captions)],
                'attribution': attributions[index % len(attributions)],
            })
        return None

    def _create_block_quote(self, index):
        """Create a block quote with fixed content."""
        quote_texts = [
            'The secret to great bread is patience and quality ingredients.',
            'Baking is both an art and a science, requiring precision and creativity.',
            'Every loaf tells a story of tradition and craftsmanship.',
            'The best bread comes from the heart, not just the recipe.',
            'In baking, timing is everything.',
        ]
        attribute_names = [
            'Master Baker',
            'Artisan Chef',
            'Bread Expert',
            'Culinary Professional',
            'Baking Specialist',
        ]
        themes = ['default', 'highlight']
        text_sizes = ['default', 'large']
        
        return ('block_quote', {
            'text': quote_texts[index % len(quote_texts)],
            'attribute_name': attribute_names[index % len(attribute_names)],
            'settings': {
                'theme': themes[index % len(themes)],
                'text_size': text_sizes[index % len(text_sizes)]
            }
        })

    def generate_streamfield(self, num_blocks, num_paragraphs=0):
        """Generate StreamField blocks cycling through heading, block_quote, paragraph, image."""
        blocks = []
        block_sequence = [
            lambda i: self._create_heading_block(i),      # 0
            lambda i: self._create_block_quote(i),        # 1
            lambda i: self._create_heading_block(i),      # 2
            lambda i: self._create_image_block(i) or self._create_paragraph_block(i),  # 3
            lambda i: self._create_paragraph_block(i, 2 if num_paragraphs > 0 else 1),  # 4
        ]

        for i in range(num_blocks):
            block_creator = block_sequence[i % 5]
            blocks.append(block_creator(i))

        return blocks

    def _publish_page_with_revisions(self, page, revisions):
        """Publish page and create additional draft revisions."""
        original_introduction = page.introduction

        revision = page.save_revision()
        revision.publish()
        page.refresh_from_db()

        for rev_num in range(revisions - 1):
            page.introduction = f"[Revision {rev_num + 2}] " + original_introduction
            page.save_revision()

        page.introduction = original_introduction
        page.refresh_from_db()


    def create_blog_pages(self, home_page, count):
        """Create blog pages with relationships, tags, and streamfield content."""
        blog_index = BlogIndexPage.objects.filter(slug='blog').first()
        if not blog_index:
            self.stdout.write(self.style.WARNING('  Blog index not found. Skipping blog pages.'))
            return 0

        people = list(Person.objects.all())
        if not people and INLINE_PANEL_ITEMS > 0:
            self.stdout.write(self.style.WARNING('  No Person objects found. Creating sample people.'))
            now = timezone.now()
            images = self._get_images_cache()
            
            # Fixed names and job titles for consistent benchmark data
            first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Jessica', 'William', 'Ashley']
            last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Wilson', 'Moore']
            job_titles = ['Senior Developer', 'Product Manager', 'Design Lead', 'Content Writer', 'Marketing Specialist']
            
            num_people = max(10, INLINE_PANEL_ITEMS)
            people_to_create = []
            for i in range(num_people):
                person = Person(
                    first_name=first_names[i % len(first_names)],
                    last_name=last_names[i % len(last_names)],
                    job_title=job_titles[i % len(job_titles)],
                    live=True,
                    first_published_at=now,
                    last_published_at=now,
                    image=images[i % len(images)] if images else None,
                )
                people_to_create.append(person)
            Person.objects.bulk_create(people_to_create)
            people = list(Person.objects.all())

        # Assign images to existing Person objects that don't have images
        people_without_images = [p for p in people if not p.image]
        if people_without_images:
            images = self._get_images_cache()
            if images:
                for i, person in enumerate(people_without_images):
                    person.image = images[i % len(images)]
                Person.objects.bulk_update(people_without_images, ['image'])
                # Refresh the people list
                people = list(Person.objects.all())

        start_number = BlogPage.objects.count() + 1

        tag_names = ['baking', 'bread', 'recipe', 'cooking', 'food', 'bakery', 'yeast', 'dough', 'pastry', 'dessert']
        tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]

        body = self.generate_streamfield(STREAMFIELD_BLOCKS, RICH_TEXT_PARAGRAPHS)

        created_count = 0
        for i in range(count):
            page_number = start_number + i
            title = f"Blog Post {page_number}"
            slug = slugify(title)

            if BlogPage.objects.filter(slug=slug).exists():
                continue

            with transaction.atomic():
                page = BlogPage(
                    title=title,
                    slug=slug,
                    subtitle=lorem_ipsum.words(random.randint(5, 12), common=False),
                    introduction=self._generate_paragraph(),
                    body=body,
                    image=self.get_random_image(),
                    date_published=date.today(),
                )
                blog_index.add_child(instance=page)
                page.refresh_from_db()

                if people:
                    selected_person = random.choice(people)
                    BlogPersonRelationship.objects.create(
                        page=page,
                        person=selected_person
                    )

                if tags:
                    page.tags.add(*random.sample(tags, min(random.randint(2, 5), len(tags))))

                self._publish_page_with_revisions(page, REVISIONS_PER_PAGE)
                created_count += 1

        return created_count

    def create_bread_pages(self, home_page, count):
        """Create bread pages with random types, origins, and ingredients."""
        breads_index = BreadsIndexPage.objects.filter(slug='breads').first()
        if not breads_index:
            self.stdout.write(self.style.WARNING('  Breads index not found. Skipping bread pages.'))
            return 0

        bread_type_names = ['Sourdough', 'Baguette', 'Ciabatta', 'Rye', 'Whole Wheat',
                            'Multigrain', 'Pumpernickel', 'Focaccia', 'Challah', 'Brioche',
                            'Naan', 'Pita', 'Cornbread', 'Flatbread', 'Tortilla']
        country_names = ['France', 'Italy', 'Germany', 'United States', 'United Kingdom',
                         'Spain', 'Greece', 'Turkey', 'India', 'Mexico', 'Canada', 'Australia']
        ingredient_names = ['Flour', 'Water', 'Yeast', 'Salt', 'Sugar', 'Olive Oil',
                            'Butter', 'Eggs', 'Milk', 'Honey', 'Seeds', 'Nuts']

        bread_types = [BreadType.objects.get_or_create(title=name)[0] for name in bread_type_names]
        countries = [Country.objects.get_or_create(title=name)[0] for name in country_names]
        ingredients = [BreadIngredient.objects.get_or_create(name=name)[0] for name in ingredient_names]

        start_number = BreadPage.objects.count() + 1
        body = self.generate_streamfield(STREAMFIELD_BLOCKS)

        created_count = 0
        for i in range(count):
            page_number = start_number + i
            title = f"{random.choice(bread_type_names)} #{page_number}"
            slug = slugify(title)

            if BreadPage.objects.filter(slug=slug).exists():
                continue

            with transaction.atomic():
                page = BreadPage(
                    title=title,
                    slug=slug,
                    introduction=self._generate_paragraph(),
                    body=body,
                    bread_type=random.choice(bread_types),
                    origin=random.choice(countries) if countries else None,
                    image=self.get_random_image(),
                )
                breads_index.add_child(instance=page)
                page.refresh_from_db()

                if ingredients:
                    page.ingredients.set(random.sample(ingredients, min(random.randint(3, 8), len(ingredients))))

                self._publish_page_with_revisions(page, REVISIONS_PER_PAGE)
                created_count += 1

        return created_count

    def _generate_location_address(self, city):
        """Generate a random address for the given city."""
        street_number = random.randint(1, 999)
        street_name = random.choice(['Main Street', 'Oak Avenue', 'Park Road', 'High Street', 'Church Lane'])
        country = random.choice(['Iceland', 'United States', 'United Kingdom', 'France', 'Germany'])
        return f"{street_number} {street_name},\r\n{city},\r\n{country}"

    def _generate_lat_long(self):
        """Generate random latitude and longitude coordinates."""
        lat = random.uniform(-90, 90)
        lng = random.uniform(-180, 180)
        return f"{lat:.6f}, {lng:.6f}"

    def _create_operating_hours(self, page):
        """Create operating hours for all days of the week"""
        # Define hours for weekdays and weekends
        weekday_hours = {'opening': time(9, 0), 'closing': time(17, 0)}
        weekend_hours = {'opening': time(10, 0), 'closing': time(16, 0)}
        
        # Map days to their respective hours
        days_config = {
            'MON': weekday_hours,
            'TUE': weekday_hours,
            'WED': weekday_hours,
            'THU': weekday_hours,
            'FRI': weekday_hours,
            'SAT': weekend_hours,
            'SUN': weekend_hours,
        }
        
        # Create operating hours using a loop
        operating_hours = [
            LocationOperatingHours(
                location=page,
                day=day,
                opening_time=hours['opening'],
                closing_time=hours['closing'],
                closed=False
            )
            for day, hours in days_config.items()
        ]
        LocationOperatingHours.objects.bulk_create(operating_hours)

    def create_location_pages(self, home_page, count):
        """Create location pages with addresses, coordinates, and operating hours."""
        locations_index = LocationsIndexPage.objects.filter(slug='locations').first()
        if not locations_index:
            self.stdout.write(self.style.WARNING('  Locations index not found. Skipping location pages.'))
            return 0

        cities = ['New York', 'London', 'Paris', 'Tokyo', 'Sydney', 'Berlin',
                  'Toronto', 'Mumbai', 'Singapore', 'Dubai', 'Barcelona', 'Amsterdam',
                  'Rome', 'Madrid', 'Seoul', 'San Francisco', 'Chicago', 'Boston']

        start_number = LocationPage.objects.count() + 1
        body = self.generate_streamfield(STREAMFIELD_BLOCKS)

        created_count = 0
        for i in range(count):
            city = random.choice(cities)
            title = f"{city} Location #{start_number + i}"
            slug = slugify(title)

            if LocationPage.objects.filter(slug=slug).exists():
                continue

            with transaction.atomic():
                page = LocationPage(
                    title=title,
                    slug=slug,
                    introduction=self._generate_paragraph(),
                    body=body,
                    address=self._generate_location_address(city),
                    lat_long=self._generate_lat_long(),
                    image=self.get_random_image(),
                )
                locations_index.add_child(instance=page)
                page.refresh_from_db()

                self._create_operating_hours(page)
                self._publish_page_with_revisions(page, REVISIONS_PER_PAGE)
                created_count += 1

        return created_count
