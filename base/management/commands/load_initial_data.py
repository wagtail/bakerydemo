import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.management import call_command
from django.core.management.base import BaseCommand
from wagtail.models import Page, Site


class Command(BaseCommand):
    def _copy_files(self, local_storage, path):
        """
        Recursively copy files from local_storage to default_storage. Used
        to automatically bootstrap the media directory (both locally and on
        cloud providers) with the images linked from the initial data (and
        included in MEDIA_ROOT).
        """
        directories, file_names = local_storage.listdir(path)
        for directory in directories:
            self._copy_files(local_storage, path + directory + "/")
        for file_name in file_names:
            with local_storage.open(path + file_name) as file_:
                default_storage.save(path + file_name, file_)

    def handle(self, **options):
        fixtures_dir = os.path.join(settings.PROJECT_DIR, "base", "fixtures")
        fixture_file = os.path.join(fixtures_dir, "bakerydemo.json")

        print("Copying media files to configured storage...")  # noqa: T201
        local_storage = FileSystemStorage(os.path.join(fixtures_dir, "media"))
        self._copy_files(local_storage, "")  # file storage paths are relative

        # Wagtail creates default Site and Page instances during install, but we already have
        # them in the data load. Remove the auto-generated ones.
        if Site.objects.filter(hostname="localhost").exists():
            Site.objects.get(hostname="localhost").delete()
        if Page.objects.filter(title="Welcome to your new Wagtail site!").exists():
            Page.objects.get(title="Welcome to your new Wagtail site!").delete()

        call_command("loaddata", fixture_file, verbosity=0)
        call_command("update_index", verbosity=0)
        call_command("rebuild_references_index", verbosity=0)

        print(  # noqa: T201
            "Awesome. Your data is loaded! The bakery's doors are almost ready to open..."
        )
