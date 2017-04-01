import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command

from wagtail.wagtailcore.models import Site

class Command(BaseCommand):
    def handle(self, **options):
        fixtures_dir = os.path.join(settings.BASE_DIR, 'base', 'fixtures')
        fixture_file = os.path.join(fixtures_dir, 'bakerydemo.json')

        call_command('loaddata', fixture_file, verbosity=0)

        # Wagtail creates a Site instance during initial load, but we already have
        # one in the data load. Both point to the same root document, so remove the auto-generated one.
        if Site.objects.filter(hostname='localhost').exists():
            Site.objects.get(hostname='localhost').delete()

        print("Awesome. Your data is loaded! The bakery's doors are almost ready to open...")
