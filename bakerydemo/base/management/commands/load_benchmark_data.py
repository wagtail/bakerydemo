"""
Management command to load benchmark data for performance testing.
"""
import random
from datetime import date, time

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import lorem_ipsum, timezone
from django.utils.text import slugify
from taggit.models import Tag
from wagtail.images.models import Image
from wagtail.rich_text import RichText

from bakerydemo.base.models import Person
from bakerydemo.blog.models import BlogIndexPage, BlogPage, BlogPersonRelationship
from bakerydemo.breads.models import BreadIngredient, BreadPage, BreadsIndexPage, BreadType, Country
from bakerydemo.locations.models import LocationOperatingHours, LocationPage, LocationsIndexPage


class Command(BaseCommand):
    help = 'Load benchmark data for performance testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--blog-pages',
            type=int,
            default=10000,
            help='Number of blog pages to create (default: 10000, for 100K scale use 33334)',
        )
        parser.add_argument(
            '--bread-pages',
            type=int,
            default=10000,
            help='Number of bread pages to create (default: 10000, for 100K scale use 33333)',
        )
        parser.add_argument(
            '--location-pages',
            type=int,
            default=10000,
            help='Number of location pages to create (default: 10000, for 100K scale use 33333)',
        )
        parser.add_argument(
            '--streamfield-blocks',
            type=int,
            default=100,
            help='Number of blocks in each StreamField (default: 100)',
        )
        parser.add_argument(
            '--streamfield-depth',
            type=int,
            default=10,
            help='Nesting depth for StreamField blocks (default: 10, max: 10)',
        )
        parser.add_argument(
            '--inline-panel-items',
            type=int,
            default=100,
            help='Number of inline panel items to create (default: 100)',
        )
        parser.add_argument(
            '--rich-text-paragraphs',
            type=int,
            default=100,
            help='Number of paragraphs in rich text fields (default: 100)',
        )
        parser.add_argument(
            '--revisions-per-page',
            type=int,
            default=34,
            help='Number of revisions per page (default: 34, for 1M total with 30K pages)',
        )
        parser.add_argument(
            '--page-tree-depth',
            type=int,
            default=1,
            help='Depth of page tree hierarchy (default: 1, max: 10)',
        )
        parser.add_argument(
            '--create-images',
            type=int,
            default=0,
            help='Number of images to create (default: 0, for scale testing use 10000)',
        )
        parser.add_argument(
            '--create-snippets',
            action='store_true',
            help='Create 1M snippet instances (BreadType, Country, BreadIngredient)',
        )

    def handle(self, *args, **options):
        self.blog_pages = options['blog_pages']
        self.bread_pages = options['bread_pages']
        self.location_pages = options['location_pages']
        self.streamfield_blocks = options['streamfield_blocks']
        self.streamfield_depth = min(options['streamfield_depth'], 10)
        self.inline_panel_items = options['inline_panel_items']
        self.rich_text_paragraphs = options['rich_text_paragraphs']
        self.revisions_per_page = options['revisions_per_page']
        self.page_tree_depth = min(options['page_tree_depth'], 10)
        self.create_images = options['create_images']
        self.create_snippets = options['create_snippets']

        self.stdout.write('Starting benchmark data generation...')

        # Create images if requested
        if self.create_images > 0:
            created = self.create_benchmark_images(self.create_images)
            self.stdout.write(f'Created {created} images')

        # Create snippets if requested
        if self.create_snippets:
            created = self.create_benchmark_snippets()
            self.stdout.write(f'Created {created} snippet instances')

        created = self.create_blog_pages(self.blog_pages)
        self.stdout.write(f'Created {created} blog pages')

        created = self.create_bread_pages(self.bread_pages)
        self.stdout.write(f'Created {created} bread pages')

        created = self.create_location_pages(self.location_pages)
        self.stdout.write(f'Created {created} location pages')

        self.stdout.write('Benchmark data generation complete!')

    def _get_images_cache(self):
        """Cache images to avoid repeated queries."""
        if not hasattr(self, '_images_cache'):
            self._images_cache = list(Image.objects.all())
        return self._images_cache

    def create_benchmark_images(self, count):
        """Create benchmark images with solid color placeholders."""
        from io import BytesIO
        from PIL import Image as PILImage
        from django.core.files.uploadedfile import InMemoryUploadedFile

        created_count = 0
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
            (255, 0, 255), (0, 255, 255), (128, 128, 128), (255, 128, 0),
        ]

        for i in range(count):
            title = f"Benchmark Image {i + 1}"

            if Image.objects.filter(title=title).exists():
                continue

            # Create a simple colored image
            img = PILImage.new('RGB', (800, 600), color=colors[i % len(colors)])
            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=85)
            img_io.seek(0)

            img_file = InMemoryUploadedFile(
                img_io, None, f'benchmark_{i + 1}.jpg', 'image/jpeg',
                img_io.getbuffer().nbytes, None
            )

            wagtail_image = Image(
                title=title,
                file=img_file,
            )
            wagtail_image.save()
            created_count += 1

            if created_count % 100 == 0:
                self.stdout.write(f'  Created {created_count} images...')

        # Clear the cache so new images are picked up
        if hasattr(self, '_images_cache'):
            del self._images_cache

        return created_count

    def create_benchmark_snippets(self):
        """Create 1M snippet instances (BreadType, Country, BreadIngredient)."""
        created_count = 0
        batch_size = 1000

        # Create BreadType snippets (~333K)
        self.stdout.write('  Creating BreadType snippets...')
        bread_types = []
        for i in range(333334):
            bread_types.append(BreadType(title=f"Bread Type {i + 1}"))
            if len(bread_types) >= batch_size:
                BreadType.objects.bulk_create(bread_types, ignore_conflicts=True)
                created_count += len(bread_types)
                bread_types = []
                if created_count % 10000 == 0:
                    self.stdout.write(f'    Created {created_count} snippets...')
        if bread_types:
            BreadType.objects.bulk_create(bread_types, ignore_conflicts=True)
            created_count += len(bread_types)

        # Create Country snippets (~333K)
        self.stdout.write('  Creating Country snippets...')
        countries = []
        for i in range(333333):
            countries.append(Country(title=f"Country {i + 1}"))
            if len(countries) >= batch_size:
                Country.objects.bulk_create(countries, ignore_conflicts=True)
                created_count += len(countries)
                countries = []
                if created_count % 10000 == 0:
                    self.stdout.write(f'    Created {created_count} snippets...')
        if countries:
            Country.objects.bulk_create(countries, ignore_conflicts=True)
            created_count += len(countries)

        # Create BreadIngredient snippets (~333K)
        self.stdout.write('  Creating BreadIngredient snippets...')
        ingredients = []
        for i in range(333333):
            ingredients.append(BreadIngredient(name=f"Ingredient {i + 1}"))
            if len(ingredients) >= batch_size:
                BreadIngredient.objects.bulk_create(ingredients, ignore_conflicts=True)
                created_count += len(ingredients)
                ingredients = []
                if created_count % 10000 == 0:
                    self.stdout.write(f'    Created {created_count} snippets...')
        if ingredients:
            BreadIngredient.objects.bulk_create(ingredients, ignore_conflicts=True)
            created_count += len(ingredients)

        return created_count

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
        # Repeat paragraphs to reach the desired count
        paragraphs_to_use = []
        for i in range(num_paragraphs):
            paragraphs_to_use.append(fixed_paragraphs[i % len(fixed_paragraphs)])
        paragraph_text = '\n'.join(paragraphs_to_use)
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

    def generate_streamfield(self, num_blocks, num_paragraphs=0, depth=0):
        """Generate StreamField blocks with optional nesting depth."""
        blocks = []

        # If we have depth remaining and blocks to create, add nested blocks
        if depth > 0 and num_blocks > 0:
            # Create nested structure blocks - not all block types support nesting
            # For simplicity, we'll create paragraph blocks that could conceptually be nested
            for i in range(min(num_blocks, 10)):  # Limit nested blocks per level
                blocks.append(self._create_paragraph_block(i, num_paragraphs if num_paragraphs > 0 else 2))

            # Recursively add nested blocks
            if depth > 1 and num_blocks > 10:
                # Create a marker for nesting (in real implementation, this would be a StructBlock)
                nested_blocks = self.generate_streamfield(num_blocks // 2, num_paragraphs, depth - 1)
                # In a real implementation with proper StructBlock support, we'd wrap these
                # For now, just add them to demonstrate the nesting capability
                blocks.extend(nested_blocks[:min(len(nested_blocks), num_blocks - 10)])
        else:
            # Regular flat block structure
            block_sequence = [
                lambda i: self._create_heading_block(i),
                lambda i: self._create_block_quote(i),
                lambda i: self._create_heading_block(i),
                lambda i: self._create_image_block(i) or self._create_paragraph_block(i, num_paragraphs if num_paragraphs > 0 else 2),
                lambda i: self._create_paragraph_block(i, num_paragraphs if num_paragraphs > 0 else 2),
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


    def create_blog_pages(self, count):
        """Create blog pages with relationships, tags, and streamfield content."""
        blog_index = BlogIndexPage.objects.filter(slug='blog').first()
        if not blog_index:
            self.stdout.write(self.style.WARNING('  Blog index not found. Skipping blog pages.'))
            return 0

        people = list(Person.objects.all())
        if not people and self.inline_panel_items > 0:
            # ...existing code for creating people...
            self.stdout.write(self.style.WARNING('  No Person objects found. Creating sample people.'))
            now = timezone.now()
            images = self._get_images_cache()

            # Fixed names and job titles for consistent benchmark data
            first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Jessica', 'William', 'Ashley']
            last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Wilson', 'Moore']
            job_titles = ['Senior Developer', 'Product Manager', 'Design Lead', 'Content Writer', 'Marketing Specialist']

            num_people = max(10, self.inline_panel_items)
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

        body = self.generate_streamfield(self.streamfield_blocks, self.rich_text_paragraphs, self.streamfield_depth)

        created_count = 0
        current_parent = blog_index
        pages_at_current_level = []

        for i in range(count):
            page_number = start_number + i
            title = f"Blog Post {page_number}"
            slug = slugify(title)

            if BlogPage.objects.filter(slug=slug).exists():
                continue

            # Implement tree depth: create hierarchy of pages
            level = 1
            if self.page_tree_depth > 1:
                # Calculate which level this page should be at
                level = (i % self.page_tree_depth) + 1

                if level == 1:
                    current_parent = blog_index
                    pages_at_current_level = []
                elif level > 1 and pages_at_current_level:
                    # Use the last page from previous level as parent
                    current_parent = pages_at_current_level[-1]

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
                current_parent.add_child(instance=page)
                page.refresh_from_db()

                if people:
                    selected_person = random.choice(people)
                    BlogPersonRelationship.objects.create(
                        page=page,
                        person=selected_person
                    )

                if tags:
                    page.tags.add(*random.sample(tags, min(random.randint(2, 5), len(tags))))

                self._publish_page_with_revisions(page, self.revisions_per_page)
                created_count += 1

                # Track pages at current level for hierarchy
                if self.page_tree_depth > 1:
                    if level == len(pages_at_current_level) + 1:
                        pages_at_current_level.append(page)
                    elif level <= len(pages_at_current_level):
                        pages_at_current_level = pages_at_current_level[:level-1] + [page]

        return created_count

    def create_bread_pages(self, count):
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
        body = self.generate_streamfield(self.streamfield_blocks, 0, self.streamfield_depth)

        created_count = 0
        current_parent = breads_index
        pages_at_current_level = []

        for i in range(count):
            page_number = start_number + i
            title = f"{random.choice(bread_type_names)} #{page_number}"
            slug = slugify(title)

            if BreadPage.objects.filter(slug=slug).exists():
                continue

            # Implement tree depth
            level = 1
            if self.page_tree_depth > 1:
                level = (i % self.page_tree_depth) + 1
                if level == 1:
                    current_parent = breads_index
                    pages_at_current_level = []
                elif level > 1 and pages_at_current_level:
                    current_parent = pages_at_current_level[-1]

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
                current_parent.add_child(instance=page)
                page.refresh_from_db()

                if ingredients:
                    page.ingredients.set(random.sample(ingredients, min(random.randint(3, 8), len(ingredients))))

                self._publish_page_with_revisions(page, self.revisions_per_page)
                created_count += 1

                if self.page_tree_depth > 1:
                    if level == len(pages_at_current_level) + 1:
                        pages_at_current_level.append(page)
                    elif level <= len(pages_at_current_level):
                        pages_at_current_level = pages_at_current_level[:level-1] + [page]

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

    def create_location_pages(self, count):
        """Create location pages with addresses, coordinates, and operating hours."""
        locations_index = LocationsIndexPage.objects.filter(slug='locations').first()
        if not locations_index:
            self.stdout.write(self.style.WARNING('  Locations index not found. Skipping location pages.'))
            return 0

        cities = ['New York', 'London', 'Paris', 'Tokyo', 'Sydney', 'Berlin',
                  'Toronto', 'Mumbai', 'Singapore', 'Dubai', 'Barcelona', 'Amsterdam',
                  'Rome', 'Madrid', 'Seoul', 'San Francisco', 'Chicago', 'Boston']

        start_number = LocationPage.objects.count() + 1
        body = self.generate_streamfield(self.streamfield_blocks, 0, self.streamfield_depth)

        created_count = 0
        current_parent = locations_index
        pages_at_current_level = []

        for i in range(count):
            city = random.choice(cities)
            title = f"{city} Location #{start_number + i}"
            slug = slugify(title)

            if LocationPage.objects.filter(slug=slug).exists():
                continue

            # Implement tree depth
            level = 1
            if self.page_tree_depth > 1:
                level = (i % self.page_tree_depth) + 1
                if level == 1:
                    current_parent = locations_index
                    pages_at_current_level = []
                elif level > 1 and pages_at_current_level:
                    current_parent = pages_at_current_level[-1]

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
                current_parent.add_child(instance=page)
                page.refresh_from_db()

                self._create_operating_hours(page)
                self._publish_page_with_revisions(page, self.revisions_per_page)
                created_count += 1

                if self.page_tree_depth > 1:
                    if level == len(pages_at_current_level) + 1:
                        pages_at_current_level.append(page)
                    elif level <= len(pages_at_current_level):
                        pages_at_current_level = pages_at_current_level[:level-1] + [page]

        return created_count
