"""
Management command to load benchmark data for performance testing.
"""
import random
from datetime import date
from io import BytesIO

from PIL import Image as PILImage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum, timezone
from wagtail.images.models import Image
from wagtail.models import Locale
from wagtail.rich_text import RichText

from bakerydemo.base.models import Person
from bakerydemo.blog.models import BlogIndexPage, BlogPage, BlogPersonRelationship
from bakerydemo.breads.models import BreadIngredient, BreadType, Country


class Command(BaseCommand):
    help = 'Load benchmark data for performance testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--blog-pages-count',
            type=int,
            default=100000,
            help='Number of blog pages to create',
        )
        parser.add_argument(
            '--streamfield-blocks-count',
            type=int,
            default=100,
            help='Number of blocks in each StreamField',
        )
        parser.add_argument(
            '--streamfield-depth',
            type=int,
            default=10,
            help='Nesting depth for StreamField blocks',
        )
        parser.add_argument(
            '--inline-panel-items-count',
            type=int,
            default=100,
            help='Number of inline panel items to create',
        )
        parser.add_argument(
            '--paragraphs-count',
            type=int,
            default=100,
            help='Number of paragraphs in rich text fields',
        )
        parser.add_argument(
            '--revisions-per-page-count',
            type=int,
            default=100000,
            help='Number of revisions per page',
        )
        parser.add_argument(
            '--page-tree-depth',
            type=int,
            default=10,
            help='Depth of page tree hierarchy',
        )
        parser.add_argument(
            '--images-count',
            type=int,
            default=100,
            help='Number of images to create',
        )
        parser.add_argument(
            '--snippets-count',
            type=int,
            default=100000,
            help='Number of snippet instances to create',
        )
        parser.add_argument(
            '--translations-count',
            type=int,
            default=100,
            help='Number of language translations to create',
        )

    def handle(self, *args, **options):
        self.set_input_params(options)
        self.print_configurations()

        self.create_benchmark_images()
        self.create_blog_pages()
        self.create_inline_panel_items()
        self.create_benchmark_snippets()
        self.create_revisionss()
        self.create_translations()
        self.generate_streamfield(self.streamfield_blocks_count, self.paragraphs_count, self.streamfield_depth)

        self.stdout.write(self.style.SUCCESS('\n=== Benchmark Data Generation Complete! ==='))

    def set_input_params(self, options):
        self.blog_pages_count = options['blog_pages_count']
        self.streamfield_blocks_count = options['streamfield_blocks_count']
        self.streamfield_depth = min(options['streamfield_depth'], 10)
        self.inline_panel_items_count = options['inline_panel_items_count']
        self.paragraphs_count = options['paragraphs_count']
        self.revisions_per_page_count = options['revisions_per_page_count']
        self.page_tree_depth = min(options['page_tree_depth'], 10)
        self.images_count = options['images_count']
        self.snippets_count = options['snippets_count']
        self.translations_count = min(options['translations_count'], 100)

    def print_configurations(self):
        self.stdout.write('\nConfiguration:')
        self.stdout.write(f'  Blog pages: {self.blog_pages_count}')
        self.stdout.write(f'  StreamField blocks: {self.streamfield_blocks_count} (depth: {self.streamfield_depth})')
        self.stdout.write(f'  Inline panel items: {self.inline_panel_items_count}')
        self.stdout.write(f'  Rich text paragraphs: {self.paragraphs_count}')
        self.stdout.write(f'  Revisions per page: {self.revisions_per_page_count}')
        self.stdout.write(f'  Page tree depth: {self.page_tree_depth}')
        self.stdout.write(f'  Images count: {self.images_count}')
        self.stdout.write(f'  Snippets count: {self.snippets_count}')
        self.stdout.write(f'  Translations count: {self.translations_count}\n')

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

        for batch_num in range((self.snippets_count + batch_size * 3 - 1) // (batch_size * 3)):
            bread_types = [BreadType(title=f"Bread Type {batch_num * batch_size + j + 1}") for j in range(batch_size)]
            BreadType.objects.bulk_create(bread_types, ignore_conflicts=True)

            countries = [Country(title=f"Country {batch_num * batch_size + j + 1}") for j in range(batch_size)]
            Country.objects.bulk_create(countries, ignore_conflicts=True)

            ingredients = [BreadIngredient(name=f"Ingredient {batch_num * batch_size + j + 1}")
                           for j in range(batch_size)]
            BreadIngredient.objects.bulk_create(ingredients, ignore_conflicts=True)

            created_count += batch_size * 3
            if created_count % (batch_size * 90) == 0:
                self.stdout.write(f'    Progress: {created_count:,} total snippets created...')

        self.stdout.write(f'Total available snippet instances are: {created_count}')

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
            'Lorem ipsum dolor st amet, consectetur adiscing elit. Sed do eimod temport labore et dolore magna aliqua.',
            'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo cequat.',
            'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
            'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt m anim id est laborum.',
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
                lambda i: self._create_image_block(i) or
                          self._create_paragraph_block(i, num_paragraphs if num_paragraphs > 0 else 2),
                lambda i: self._create_paragraph_block(i, num_paragraphs if num_paragraphs > 0 else 2),
            ]

            for i in range(num_blocks):
                block_creator = block_sequence[i % 5]
                blocks.append(block_creator(i))

        return blocks

    def create_revisionss(self):
        self.stdout.write(f'  Creating revisions for pages...')

        pages = BlogPage.objects.all()[:10]
        for page in pages:
            self.create_page_revisions(page, self.revisions_per_page_count)

    def create_page_revisions(self, page, revisions):
        """Publish page and create additional draft revisions."""
        original_introduction = page.introduction

        revision = page.save_revision()
        revision.publish()
        page.refresh_from_db()

        for rev_num in range(revisions - 1):
            page.introduction = f"[Revision {rev_num + 2}] " + original_introduction
            page.save_revision()

            if (rev_num + 1) % 1000 == 0:
                self.stdout.write(f'  Progress: {rev_num:,}/{revisions:,} revisions created for page ID {page.title}.')

        self.stdout.write(f'  ✓ Created {revisions} for page {page.title}')

        page.introduction = original_introduction
        page.refresh_from_db()

    def create_translations(self):
        """Create language translations for pages."""
        self.stdout.write(f'  Creating {self.translations_count} language translations...')

        # Generate language codes for locales (e.g., lang-01, lang-02, ..., lang-100)
        # Using synthetic language codes since we need 100 unique ones

        default_locale = Locale.objects.filter(language_code='en').first() or Locale.objects.first()
        if not default_locale:
            self.stdout.write(self.style.WARNING('  No default locale found. Skipping translations.'))
            return

        self.stdout.write('  Creating locales...')
        existing_locales = set(Locale.objects.values_list('language_code', flat=True))
        language_codes = [f"lg{i:03d}" for i in range(1, self.translations_count + 1)]

        locales_to_create = [Locale(language_code=lang_code)
                             for lang_code in language_codes if lang_code not in existing_locales]

        if locales_to_create:
            Locale.objects.bulk_create(locales_to_create, ignore_conflicts=True)
            self.stdout.write(f'  ✓ Created {len(locales_to_create)} new locales')

        locales = list(Locale.objects.filter(language_code__in=language_codes))

        blog_index = BlogIndexPage.objects.filter(slug='blog').first()
        sample_page = BlogPage.objects.first()

        if not blog_index:
            self.stdout.write(self.style.WARNING('  No blog index found. Skipping translations.'))
            return

        if not sample_page:
            self.stdout.write(self.style.WARNING('  No pages found to translate. Skipping translations.'))
            return

        # Create translations for each locale
        created_count = 0
        for locale in locales:
            try:
                # First, translate the parent page (blog index) if not already translated
                if not BlogIndexPage.objects.filter(translation_key=blog_index.translation_key, locale=locale).exists():
                    translated_index = blog_index.copy_for_translation(locale)
                    translated_index.title = f"{blog_index.title} ({locale.language_code})"
                    translated_index.save_revision().publish()

                if BlogPage.objects.filter(translation_key=sample_page.translation_key, locale=locale).exists():
                    continue

                translated_page = sample_page.copy_for_translation(locale)
                translated_page.title = f"{sample_page.title} ({locale.language_code})"
                translated_page.save_revision().publish()
                created_count += 1

                if created_count % 10 == 0:
                    self.stdout.write(f'  Progress: {created_count}/{len(locales)} translations created...')
            except Exception as e:
                self.stdout.write(f'  Error creating translation for {locale.language_code}: {str(e)[:50]}')

        self.stdout.write(f'  ✓ Created {created_count} page translations across {len(locales)} locales\n')


    def create_blog_pages(self):
        """Create blog pages with streamfield content."""
        blog_index = BlogIndexPage.objects.filter(slug='blog').first()
        if not blog_index:
            self.stdout.write(self.style.WARNING('  Blog index not found. Skipping blog pages.'))
            return

        body_template = self.generate_streamfield(1, 2, 1)
        subtitle = lorem_ipsum.words(5, common=False)
        introduction = lorem_ipsum.paragraph()
        image = self.get_random_image()
        today = date.today()

        existing_slugs = set(BlogPage.objects.values_list('slug', flat=True))
        created_count = 0
        skipped_count = 0

        start_number = BlogPage.objects.count() + 1
        self.stdout.write(f'  Creating {self.blog_pages_count:,} blog pages...')

        for i in range(self.blog_pages_count):
            page_number = start_number + i
            slug = f"blog-post-{page_number}"

            if slug in existing_slugs:
                skipped_count += 1
                continue

            page = BlogPage(
                title=f"Blog Post {page_number}",
                slug=slug,
                subtitle=subtitle,
                introduction=introduction,
                body=body_template,
                image=image,
                date_published=today,
            )

            blog_index.add_child(instance=page)
            created_count += 1

            if created_count % 1000 == 0:
                self.stdout.write(f'  Progress: {created_count:,}/{self.blog_pages_count:,} blog pages created...')

        self.stdout.write(f'  ✓ Created {created_count:,} pages (skipped {skipped_count:,} existing)')

        # Create page tree depth
        parent = blog_index
        for i in range(self.page_tree_depth):
            slug = f"blog-post-depth-{i}"
            if slug in existing_slugs:
                continue

            page = BlogPage(
                title=f"Blog Post in tree depth {i}",
                slug=slug,
                subtitle=subtitle,
                introduction=introduction,
                body=body_template,
                image=image,
                date_published=today,
            )

            parent.add_child(instance=page)
            parent = page

        self.stdout.write(f'  ✓ Created Page tree with depth {self.page_tree_depth}\n')

    def create_inline_panel_items(self):
        """Create 100 InlinePanel items for ONE page to demonstrate the requirement."""
        self.stdout.write(f'  Creating {self.inline_panel_items_count} InlinePanel items...')

        # Get or create the first blog page
        sample_page = BlogPage.objects.first()
        if not sample_page:
            self.stdout.write(self.style.WARNING('  No blog pages found. Skipping InlinePanel items.'))
            return

        # Check how many relationships already exist for this page
        existing_count = BlogPersonRelationship.objects.filter(page=sample_page).count()
        if existing_count >= self.inline_panel_items_count:
            self.stdout.write(f'  ✓ Page already has {existing_count} InlinePanel items')
            return

        # Ensure we have enough Person objects
        existing_people = Person.objects.count()
        if existing_people < self.inline_panel_items_count:
            people_to_create = []
            now = timezone.now()
            for i in range(existing_people, self.inline_panel_items_count):
                people_to_create.append(Person(
                    first_name=f"Person {i + 1}",
                    last_name="Benchmark",
                    job_title="Benchmark User",
                    live=True,
                    first_published_at=now,
                    last_published_at=now,
                ))
            Person.objects.bulk_create(people_to_create, ignore_conflicts=True)
            self.stdout.write(f'  ✓ Created {len(people_to_create)} Person objects')

        people = list(Person.objects.all()[:self.inline_panel_items_count])

        # Get existing person IDs for this page to avoid duplicates
        existing_person_ids = set(
            BlogPersonRelationship.objects.filter(page=sample_page).values_list('person_id', flat=True)
        )

        # Create relationships for the sample page
        relationships = [
            BlogPersonRelationship(page=sample_page, person=person)
            for person in people if person.id not in existing_person_ids
        ]

        if relationships:
            BlogPersonRelationship.objects.bulk_create(relationships, ignore_conflicts=True)

        total_count = BlogPersonRelationship.objects.filter(page=sample_page).count()
        self.stdout.write(f'  ✓ Page "{sample_page.title}" now has {total_count} InlinePanel items\n')
