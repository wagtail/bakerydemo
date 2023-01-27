import random
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum, timezone
from django.utils.text import slugify
from wagtail.images.models import Image
from wagtail.rich_text import RichText
from willow.image import Image as WillowImage

from bakerydemo.base.models import FooterText, HomePage, Person, StandardPage
from bakerydemo.blog.models import BlogIndexPage, BlogPage
from bakerydemo.breads.models import (
    BreadIngredient,
    BreadPage,
    BreadsIndexPage,
    BreadType,
    Country,
)
from bakerydemo.locations.models import LocationPage, LocationsIndexPage

FIXTURE_MEDIA_DIR = Path(settings.PROJECT_DIR) / "base/fixtures/media/original_images"


class Command(BaseCommand):
    help = "Creates random data. Useful for performance or load testing."

    def add_arguments(self, parser):
        parser.add_argument(
            "page_count",
            type=int,
            help="How many pages of each type to create",
        )
        parser.add_argument(
            "snippet_count",
            type=int,
            help="How many snippets of each type to create",
        )
        parser.add_argument(
            "image_count",
            type=int,
            help="How many images to create",
        )

    def fake_stream_field(self):
        return [("paragraph_block", RichText("\n".join(lorem_ipsum.paragraphs(5))))]

    def get_random_model(self, model):
        return model.objects.order_by("?").first()

    def make_title(self):
        return lorem_ipsum.words(4, common=False)

    def create_pages(self, page_count):
        self.stdout.write("Creating bread pages...")
        breads_index = BreadsIndexPage.objects.live().first()
        for _ in range(page_count):
            title = self.make_title()
            breads_index.add_child(
                instance=BreadPage(
                    title=title,
                    slug=slugify(title),
                    introduction=lorem_ipsum.paragraph(),
                    bread_type=self.get_random_model(BreadType),
                    body=self.fake_stream_field(),
                    origin=self.get_random_model(Country),
                    image=self.get_random_model(Image),
                )
            )

        self.stdout.write("Creating location pages...")
        locations_index = LocationsIndexPage.objects.live().first()
        for _ in range(page_count):
            title = self.make_title()
            locations_index.add_child(
                instance=LocationPage(
                    title=title,
                    slug=slugify(title),
                    introduction=lorem_ipsum.paragraph(),
                    image=self.get_random_model(Image),
                    address=lorem_ipsum.paragraph(),
                    body=self.fake_stream_field(),
                    lat_long="64.144367, -21.939182",
                )
            )

        self.stdout.write("Creating blog pages...")
        blog_index = BlogIndexPage.objects.live().first()
        for _ in range(page_count):
            title = self.make_title()
            blog_index.add_child(
                instance=BlogPage(
                    title=title,
                    slug=slugify(title),
                    introduction=lorem_ipsum.paragraph(),
                    body=self.fake_stream_field(),
                    subtitle=lorem_ipsum.words(10, common=False),
                    date_published=timezone.now(),
                )
            )

        self.stdout.write("Creating standard pages...")
        homepage = HomePage.objects.live().first()
        title = self.make_title()
        # Nest the standard pages under a top level one
        top_level_page = homepage.add_child(
            instance=StandardPage(
                title=title,
                slug=slugify(title),
                introduction=lorem_ipsum.paragraph(),
                image=self.get_random_model(Image),
                body=self.fake_stream_field(),
            )
        )
        for _ in range(page_count):
            title = self.make_title()
            top_level_page.add_child(
                instance=StandardPage(
                    title=title,
                    slug=slugify(title),
                    introduction=lorem_ipsum.paragraph(),
                    image=self.get_random_model(Image),
                    body=self.fake_stream_field(),
                )
            )

    def create_snippets(self, snippet_count):
        self.stdout.write("Creating countries...")
        for _ in range(snippet_count):
            Country.objects.create(title=self.make_title())

        self.stdout.write("Creating bread ingredients...")
        for _ in range(snippet_count):
            BreadIngredient.objects.create(name=self.make_title())

        self.stdout.write("Creating bread types...")
        for _ in range(snippet_count):
            BreadType.objects.create(title=self.make_title())

        self.stdout.write("Creating people...")
        for _ in range(snippet_count):
            Person.objects.create(
                first_name=lorem_ipsum.words(1, common=False),
                last_name=lorem_ipsum.words(1, common=False),
                job_title=lorem_ipsum.words(1, common=False),
                image=self.get_random_model(Image),
            )

        self.stdout.write("Creating footer text...")
        for _ in range(snippet_count):
            FooterText.objects.create(body=self.fake_stream_field())

    def create_images(self, image_count):
        image_files = list(FIXTURE_MEDIA_DIR.iterdir())

        self.stdout.write("Creating images...")
        for _ in range(image_count):
            random_image = random.choice(image_files)
            with random_image.open(mode="rb") as image_file:
                willow_image = WillowImage.open(image_file)
                width, height = willow_image.get_size()
                image = Image.objects.create(
                    title=self.make_title(),
                    width=width,
                    height=height,
                    file_size=random_image.stat().st_size,
                )
                image_file.seek(0)
                image.file.save(random_image.name, image_file)

    def handle(self, **options):
        self.create_images(options["image_count"])
        self.create_snippets(options["snippet_count"])
        self.create_pages(options["page_count"])
