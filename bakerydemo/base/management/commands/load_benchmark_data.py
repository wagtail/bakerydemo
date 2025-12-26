"""
Management command to load benchmark data for performance testing.
"""
import random
from datetime import date, time
from io import BytesIO

from PIL import Image as PILImage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.management.base import BaseCommand
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
            '--blog-pages-count',
            type=int,
            default=1000,
            help='Number of blog pages to create (default: 33334, for 100K total)',
        )
        parser.add_argument(
            '--bread-pages-count',
            type=int,
            default=1000,
            help='Number of bread pages to create (default: 33333, for 100K total)',
        )
        parser.add_argument(
            '--location-pages-count',
            type=int,
            default=1000,
            help='Number of location pages to create (default: 33333, for 100K total)',
        )
        parser.add_argument(
            '--streamfield-blocks-count',
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
            '--inline-panel-items-count',
            type=int,
            default=100,
            help='Number of inline panel items to create (default: 100)',
        )
        parser.add_argument(
            '--rich-text-paragraphs-count',
            type=int,
            default=100,
            help='Number of paragraphs in rich text fields (default: 100)',
        )
        parser.add_argument(
            '--revisions-per-page-count',
            type=int,
            default=10000,
            help='Number of revisions per page (default: 10, for 1M total with 100K pages)',
        )
        parser.add_argument(
            '--page-tree-depth',
            type=int,
            default=10,
            help='Depth of page tree hierarchy (default: 10, max: 10)',
        )
        parser.add_argument(
            '--images-count',
            type=int,
            default=100,
            help='Number of images to create (default: 1000, range: hundreds to 10000)',
        )
        parser.add_argument(
            '--snippets-count',
            type=int,
            default=1000000,
            help='Number of snippet instances to create (default: 1000000)',
        )

    def handle(self, *args, **options):
        self.set_input_params(options)
        self.print_configurations()
        self.create_benchmark_images()
        self.create_benchmark_snippets()
        self.create_blog_pages()
        self.create_bread_pages(self.bread_pages_count)
        self.create_location_pages(self.location_pages_count)
        self.create_revisions_for_page()

        self.stdout.write(self.style.SUCCESS('\n=== Benchmark Data Generation Complete! ==='))

    def set_input_params(self, options):
        self.blog_pages_count = options['blog_pages_count']
        self.bread_pages_count = options['bread_pages_count']
        self.location_pages_count = options['location_pages_count']
        self.streamfield_blocks_count = options['streamfield_blocks_count']
        self.streamfield_depth = min(options['streamfield_depth'], 10)
        self.inline_panel_items_count = options['inline_panel_items_count']
        self.rich_text_paragraphs_count = options['rich_text_paragraphs_count']
        self.revisions_per_page_count = options['revisions_per_page_count']
        self.page_tree_depth = min(options['page_tree_depth'], 10)
        self.images_count = options['images_count']
        self.snippets_count = options['snippets_count']

    def print_configurations(self):
        self.stdout.write('\nConfiguration:')
        self.stdout.write(f'  Blog pages: {self.blog_pages_count}')
        self.stdout.write(f'  Bread pages: {self.bread_pages_count}')
        self.stdout.write(f'  Location pages: {self.location_pages_count}')
        self.stdout.write(f'  StreamField blocks: {self.streamfield_blocks_count} (depth: {self.streamfield_depth})')
        self.stdout.write(f'  Inline panel items: {self.inline_panel_items_count}')
        self.stdout.write(f'  Rich text paragraphs: {self.rich_text_paragraphs_count}')
        self.stdout.write(f'  Revisions per page: {self.revisions_per_page_count}')
        self.stdout.write(f'  Page tree depth: {self.page_tree_depth}')
        self.stdout.write(f'  Images count: {self.images_count}')
        self.stdout.write(f'  Snippets count: {self.snippets_count}\n')

    def _get_images_cache(self):
        """Cache images to avoid repeated queries."""
        if not hasattr(self, '_images_cache'):
            self._images_cache = list(Image.objects.all())
        return self._images_cache

    def create_benchmark_images(self):
        """Create benchmark images with solid color placeholders."""

        self.stdout.write('  Initializing image creation...')
        created_count = 0
        skipped_count = 0
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
            (255, 0, 255), (0, 255, 255), (128, 128, 128), (255, 128, 0),
        ]

        for i in range(self.images_count):
            title = f"Benchmark Image {i + 1}"

            if Image.objects.filter(title=title).exists():
                skipped_count += 1
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

        # Clear the cache so new images are picked up
        if hasattr(self, '_images_cache'):
            del self._images_cache
            self.stdout.write('  Cleared image cache')

        self.stdout.write(f'  Skipped {skipped_count} existing images')
        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_count} images\n'))

    def create_benchmark_snippets(self):
        """Create snippet instances (BreadType, Country, BreadIngredient)."""
        self.stdout.write('  Starting snippet creation in bulk batches...')
        created_count = 0
        batch_size = 1000

        for i in range(self.snippets_count // (batch_size * 3) + self.snippets_count % 3):
            bread_types = [BreadType(title=f"Bread Type {i * j + 1}") for j in range(batch_size)]
            BreadType.objects.bulk_create(bread_types, ignore_conflicts=True)

            countries = [Country(title=f"Country {i * j + 1}") for j in range(batch_size)]
            Country.objects.bulk_create(countries, ignore_conflicts=True)

            ingredients = [BreadIngredient(name=f"Ingredient {i * j + 1}") for j in range(batch_size)]
            BreadIngredient.objects.bulk_create(ingredients, ignore_conflicts=True)

            created_count += batch_size*3
            if created_count % 60000 == 0:
                self.stdout.write(f'    Progress: {created_count:,} total snippets created...')

        self.stdout.write(f'Created {created_count} snippet instances')

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

    def create_revisions_for_page(self):
        self.stdout.write(f'  Creating {self.revisions_per_page_count:,} revisions for a page...')

        page = BlogPage.objects.first()
        self.publish_page_with_revisions(page, self.revisions_per_page_count)

    def publish_page_with_revisions(self, page, revisions):
        """Publish page and create additional draft revisions."""
        original_introduction = page.introduction

        revision = page.save_revision()
        revision.publish()
        page.refresh_from_db()

        for rev_num in range(revisions - 1):
            page.introduction = f"[Revision {rev_num + 2}] " + original_introduction
            page.save_revision()

            # Progress every 1000 pages
            if rev_num % 1000 == 0:
                self.stdout.write(f'  Progress: {rev_num:,}/{revisions:,} revisions created...')

        page.introduction = original_introduction
        page.refresh_from_db()


    def create_blog_pages(self):
        """Create blog pages with relationships, tags, and streamfield content."""
        self.stdout.write('  Checking for blog index page...')
        blog_index = BlogIndexPage.objects.filter(slug='blog').first()
        if not blog_index:
            self.stdout.write(self.style.WARNING('  Blog index not found. Skipping blog pages.'))
            return 0
        self.stdout.write(f'  ✓ Found blog index: {blog_index.title}')

        # Only load/create 10 people objects (not 100+)
        self.stdout.write('  Loading existing Person objects...')
        people = list(Person.objects.all()[:10])
        if not people:
            self.stdout.write(self.style.WARNING('  No Person objects found. Creating 10 sample people...'))
            now = timezone.now()
            images = self._get_images_cache()[:10] if self._get_images_cache() else []

            first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Jessica', 'William', 'Ashley']
            last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Wilson', 'Moore']
            job_titles = ['Developer', 'Manager', 'Designer', 'Writer', 'Specialist']

            people_to_create = [
                Person(
                    first_name=first_names[i],
                    last_name=last_names[i],
                    job_title=job_titles[i % 5],
                    live=True,
                    first_published_at=now,
                    last_published_at=now,
                    image=images[i] if images and i < len(images) else None,
                )
                for i in range(10)
            ]
            Person.objects.bulk_create(people_to_create)
            people = list(Person.objects.all()[:10])
            self.stdout.write(f'  ✓ Created {len(people)} Person objects')
        else:
            self.stdout.write(f'  ✓ Found {len(people)} existing Person objects')

        start_number = BlogPage.objects.count() + 1
        self.stdout.write(f'  Starting page number: {start_number}')

        self.stdout.write('  Preparing tags...')
        tag_names = ['baking', 'bread', 'recipe', 'cooking', 'food']
        tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
        self.stdout.write(f'  ✓ Prepared {len(tags)} tags')

        # Create lightweight StreamField template
        self.stdout.write(f'  Generating lightweight StreamField template...')
        body_template = self.generate_streamfield(self.streamfield_blocks_count, 2, 1)
        self.stdout.write(f'  ✓ Generated StreamField template (reusable)')

        # Use add_child (required for Wagtail) but optimize by reducing operations
        self.stdout.write(f'  Creating {self.blog_pages_count:,} blog pages...')
        created_count = 0

        for i in range(self.blog_pages_count):
            page_number = start_number + i
            title = f"Blog Post {page_number}"

            page = BlogPage(
                title=title,
                slug=slugify(title),
                subtitle=lorem_ipsum.words(5, common=False),
                introduction=lorem_ipsum.paragraph(),
                body=body_template,
                image=self.get_random_image(),
                date_published=date.today(),
            )

            blog_index.add_child(instance=page)

            if people:
                BlogPersonRelationship.objects.create(
                    page=page,
                    person=people[i % len(people)]
                )

            created_count += 1

            # Progress every 1000 pages
            if created_count % 1000 == 0:
                self.stdout.write(f'  Progress: {created_count:,}/{self.blog_pages_count:,} blog pages created...')

        self.stdout.write(f'  ✓ Created {created_count:,} pages with relationships')

    def create_bread_pages(self, count):
        """Create bread pages with random types, origins, and ingredients."""
        self.stdout.write('  Checking for breads index page...')
        breads_index = BreadsIndexPage.objects.filter(slug='breads').first()
        if not breads_index:
            self.stdout.write(self.style.WARNING('  Breads index not found. Skipping bread pages.'))
            return 0
        self.stdout.write(f'  ✓ Found breads index: {breads_index.title}')

        bread_type_names = ['Sourdough', 'Baguette', 'Ciabatta', 'Rye', 'Whole Wheat']
        country_names = ['France', 'Italy', 'Germany', 'United States', 'United Kingdom']

        bread_types = [BreadType.objects.get_or_create(title=name)[0] for name in bread_type_names]
        countries = [Country.objects.get_or_create(title=name)[0] for name in country_names]

        start_number = BreadPage.objects.count() + 1
        self.stdout.write(f'  Starting page number: {start_number}')

        # Reuse lightweight StreamField template
        self.stdout.write(f'  Generating lightweight StreamField template...')
        body_template = self.generate_streamfield(self.streamfield_blocks_count, 0, 1)
        self.stdout.write(f'  ✓ Generated StreamField template')

        self.stdout.write(f'  Creating {count:,} bread pages...')
        created_count = 0

        for i in range(count):
            page_number = start_number + i
            title = f"{bread_type_names[i % len(bread_type_names)]} #{page_number}"

            page = BreadPage(
                title=title,
                slug=slugify(title),
                introduction=lorem_ipsum.paragraph(),
                body=body_template,
                bread_type=bread_types[i % len(bread_types)],
                origin=countries[i % len(countries)],
                image=self.get_random_image(),
            )

            breads_index.add_child(instance=page)
            created_count += 1

            if created_count % 1000 == 0:
                self.stdout.write(f'  Progress: {created_count:,}/{count:,} bread pages created...')

        self.stdout.write(f'  ✓ Created {created_count:,} pages')

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
        self.stdout.write('  Checking for locations index page...')
        locations_index = LocationsIndexPage.objects.filter(slug='locations').first()
        if not locations_index:
            self.stdout.write(self.style.WARNING('  Locations index not found. Skipping location pages.'))
            return 0
        self.stdout.write(f'  ✓ Found locations index: {locations_index.title}')

        cities = ['New York', 'London', 'Paris', 'Tokyo', 'Sydney', 'Berlin']

        start_number = LocationPage.objects.count() + 1
        self.stdout.write(f'  Starting page number: {start_number}')

        self.stdout.write(f'  Generating lightweight StreamField template...')
        body_template = self.generate_streamfield(min(10, self.streamfield_blocks_count), 0, 1)
        self.stdout.write(f'  ✓ Generated StreamField template')

        # Use add_child (required for Wagtail)
        self.stdout.write(f'  Creating {count:,} location pages...')
        created_count = 0

        for i in range(count):
            city = cities[i % len(cities)]
            page_number = start_number + i
            title = f"{city} Location #{page_number}"

            page = LocationPage(
                title=title,
                slug=slugify(title),
                introduction=lorem_ipsum.paragraph(),
                body=body_template,
                address=self._generate_location_address(city),
                lat_long=self._generate_lat_long(),
                image=self.get_random_image(),
            )

            locations_index.add_child(instance=page)
            created_count += 1

            if created_count % 1000 == 0:
                self.stdout.write(f'  Progress: {created_count:,}/{count:,} location pages created...')

        self.stdout.write(f'  ✓ Created {created_count:,} pages')
