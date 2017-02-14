import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, **options):
        fixtures_dir = os.path.join(settings.BASE_DIR, 'base', 'fixtures')
        fixture_file = os.path.join(fixtures_dir, 'bakerydemo.json')

        call_command('loaddata', fixture_file, verbosity=0)
        print("Awesome. Your data is loaded! The bakery's doors are almost ready to open...")
