from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum, timezone
from django.utils.text import slugify
from wagtail.rich_text import RichText
from django.core.files.base import ContentFile
from wagtail.images.models import Image
from django.db import IntegrityError
from wagtail.blocks.stream_block import StreamValue

from bakerydemo.blog.models import BlogIndexPage, BlogPage, BlogPersonRelationship
from bakerydemo.base.models import Person
from bakerydemo.base.blocks import BlockQuote, ImageBlock
import requests
import json
import random
import datetime
import string
from wagtail.models import Collection

from openai import OpenAI

FIXTURE_MEDIA_DIR = Path(settings.PROJECT_DIR) / "base/fixtures/media/original_images"
client = OpenAI()

class Command(BaseCommand):
    help = "Creates generated Page data using chatGPT. Useful for demonstrating different use cases."

    def add_arguments(self, parser):
        parser.add_argument(
            "--page_count",
            type=int,
            help="How many blog pages to create",
        )

    def make_stream_field_content(self, title, subtitle, collection_name):
        # get random images for the blog from the generated set
        image_1 = self.get_random_image(Image, collection_name)
        image_2 = self.get_random_image(Image, collection_name)
        # generate rich text for the content
        prompt = f"""Please give me three paragraphs of content for a blog post called '{title}' with the subtitle '{subtitle}'. They should in JSON of the form {{"paragraph_1": "<p>example</p>", "paragraph_2": "<p>example</p>", "paragraph_3: "<p>example<p>"}} where example is replaced with html content. You may use <p>,<h2>,<h3> and <h4> tags as well as lists. It is the entire blog post so make sure to conclude at the end."""
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4",
        )
        streamfield_chat_completion = chat_completion.choices[0].message.content.replace('\n', "")
        json_streamfield_chat_completion = json.loads(streamfield_chat_completion)

        return [('paragraph_block', RichText(json_streamfield_chat_completion["paragraph_1"])),
                ('image_block', {'image': image_1}),
                ('paragraph_block', RichText(json_streamfield_chat_completion["paragraph_2"])),
                ('image_block', {'image': image_2}),
                ('paragraph_block', RichText(json_streamfield_chat_completion["paragraph_3"])),
                ]


    def generate_images(self, theme, number_of_images, collection_name):
        for _ in range(number_of_images):
            print("Generating image...")
            prompt = f"an image for blog post about {theme}"
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            # Download the image
            image_url = response.data[0].url
            response = requests.get(image_url)
            # Get or create a collection for the generated images
            try:
                collection, created = Collection.objects.get_or_create(name=collection_name)
            except IntegrityError:
                root_coll = Collection.get_first_root_node()
                collection = root_coll.add_child(name=collection_name)

            if response.status_code == 200:
                # Create a Django ContentFile with the image content
                image_content = ContentFile(response.content)
                wagtail_image = Image(title=prompt, collection=collection)
                wagtail_image.file.save(f"{prompt}.jpg", image_content, save=True)

    def make_title(self, theme):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Create a unique and creative title for a blog post about {theme}. Aim for originality and surprise me with your choice. It should be of the format title: subtitle. Don't include the words title or subtitle in your response",
                }
            ],
            model="gpt-4",
        )
        content = chat_completion.choices[0].message.content.strip("'").strip('"')
        title, subtitle = content.split(":", 1)
        print(f'title: {title}, subtitle: {subtitle}')
        return title, subtitle

    def make_intro(self, title, subtitle):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Based on the title '{title}' and the subtitle '{subtitle}', create an introduction paragraph for this blog post. Don't repeat the title or the subtitle.",
                }
            ],
            model="gpt-4",
        )
        content = chat_completion.choices[0].message.content.strip("'")
        return content

    def get_random_image(self, model, collection_name):
        return model.objects.filter(collection__name=collection_name).order_by("?").first()

    def get_random_model(self, model):
        return model.objects.order_by("?").first()

    def get_random_recent_date(self):
        now = timezone.now()
        random_day_diff = random.randint(0, 365)
        random_date = now - datetime.timedelta(days=random_day_diff)
        return random_date

    def create_pages(self, page_count, theme, collection_name):
        self.stdout.write("Creating blog pages...")
        blog_index = BlogIndexPage.objects.live().first()
        for _ in range(page_count):
            title, subtitle = self.make_title(theme)
            new_blog_page = BlogPage(
                    title=title,
                    image=self.get_random_image(Image, collection_name),
                    slug=slugify(title),
                    introduction=self.make_intro(title, subtitle),
                    body=self.make_stream_field_content(title, subtitle, collection_name),
                    subtitle=subtitle,
                    date_published=self.get_random_recent_date(),
                )
            blog_index.add_child(instance=new_blog_page)
            # add an author
            BlogPersonRelationship.objects.create(page=new_blog_page, person=self.get_random_model(Person))

    def handle(self, **options):
        theme = input('What should the blog posts be about? ')
        page_count = int(input('How many blog posts should be created? '))
        generate_images = input('Do you want to create new images? (y/n): ').lower().strip()
        if generate_images == 'y':
            number_of_images = int(input('How many images should be created? '))
            collection_name = input('What should the collection to keep these images in be called? (Or what is the name of an existing one?) ')
        else:
            number_of_images = 0
            collection_name = input('Which collection do you want to take images from? ')
        self.generate_images(theme, number_of_images, collection_name)
        self.create_pages(page_count, theme, collection_name)
