import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command

from wagtail.core.models import Site, Page


class Command(BaseCommand):
    def handle(self, **options):
        fixtures_dir = os.path.join(settings.PROJECT_DIR, 'base', 'fixtures')
        fixture_file = os.path.join(fixtures_dir, 'bakerydemo.json')

        # Wagtail creates default Site and Page instances during install, but we already have
        # them in the data load. Remove the auto-generated ones.
        if Site.objects.filter(hostname='localhost').exists():
            Site.objects.get(hostname='localhost').delete()
        if Page.objects.filter(title='Welcome to your new Wagtail site!').exists():
            Page.objects.get(title='Welcome to your new Wagtail site!').delete()

        call_command('loaddata', fixture_file, verbosity=0)

        print("Awesome. Your data is loaded! The bakery's doors are almost ready to open...")
