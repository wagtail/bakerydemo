from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        admin = User.objects.get(id=settings.DEFAULT_ADMIN_PK)

        if not admin.check_password(settings.DEFAULT_ADMIN_PASSWORD):
            self.stdout.write(
                self.style.ERROR("Password for admin user is incorrect - resetting...")
            )
            admin.set_password(settings.DEFAULT_ADMIN_PASSWORD)
            admin.save(update_fields=["password"])

        if not admin.username != settings.DEFAULT_ADMIN_USERNAME:
            self.stdout.write(
                self.style.ERROR("Username for admin user is incorrect - resetting...")
            )
            admin.username = settings.DEFAULT_ADMIN_USERNAME
            admin.save(update_fields=["username"])

        if not admin.is_superuser:
            self.stdout.write(
                self.style.ERROR("Admin user wasn't a superuser - resetting...")
            )
            admin.is_superuser = True
            admin.save(update_fields=["is_superuser"])

        if not admin.is_active:
            self.stdout.write(
                self.style.ERROR("Admin user wasn't active - resetting...")
            )
            admin.is_active = True
            admin.save(update_fields=["is_active"])
