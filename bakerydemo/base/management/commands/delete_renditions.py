from django.core.management.base import BaseCommand
from django.db import connection

# Force removal of wagtail image rendition-entries in db will force wagtail to
# regenerate renditions. Useful if renditions are removed, for instance when
# using Docker where the file system is renewed on each build.

class Command(BaseCommand):
    def handle(self, **options):
        with connection.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM wagtailimages_rendition")
            row=cursor.fetchone()
            cursor.execute("DELETE FROM wagtailimages_rendition")
            print("{} renditions removed".format(row[0]))
