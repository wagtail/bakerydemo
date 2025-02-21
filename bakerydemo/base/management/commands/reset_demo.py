from django.conf import settings
from django.core.cache import caches
from django.core.files.storage import default_storage
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS
from django_extensions.settings import POSTGRESQL_ENGINES
from wagtail.documents import get_document_model
from wagtail.images import get_image_model


class Command(BaseCommand):
    def handle(self, **options):
        if settings.DATABASES[DEFAULT_DB_ALIAS]["ENGINE"] not in POSTGRESQL_ENGINES:
            raise CommandError(
                "This command can be used only with PostgreSQL databases."
            )

        # 1. (optional) Remove all objects from S3
        if "s3" in default_storage.__class__.__name__.lower():
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

        # 4. Clear caches
        for cache in caches.all():
            cache.clear()

        # 5. Re-import data
        call_command("load_initial_data")

        # 6. Change the admin password (in case it's different in this environment)
        call_command("reset_admin_password")
