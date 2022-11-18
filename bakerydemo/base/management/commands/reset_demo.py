from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management import call_command
from django.core.management.base import BaseCommand
from wagtail.documents import get_document_model
from wagtail.images import get_image_model


class Command(BaseCommand):
    def handle(self, **options):
        # 1. (optional) Remove all objects from S3
        if "s3" in settings.DEFAULT_FILE_STORAGE:
            self.stdout.write("Removing files from S3")
            default_storage.bucket.objects.all().delete()
        else:
            self.stdout.write("Removing images")
            get_image_model().objects.all().delete()

            self.stdout.write("Removing documents")
            get_document_model().objects.all().delete()

        # 2. Reset database to nothing
        self.stdout.write("Reset schema")
        call_command("reset_schema", interactive=False)

        # 3. Rebuild database
        call_command("migrate", interactive=False)

        # 4. Re-import data
        call_command("load_initial_data")
