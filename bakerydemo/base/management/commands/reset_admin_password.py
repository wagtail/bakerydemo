from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    DEFAULT_PASSWORD = "changeme"

    def handle(self, **options):
        admin = User.objects.get(username="admin")

        if admin.check_password(self.DEFAULT_PASSWORD):
            return

        self.stdout.write(
            self.style.ERROR("Password for admin user is incorrect - resetting...")
        )
        admin.set_password(self.DEFAULT_PASSWORD)
        admin.save(update_fields=["password"])
