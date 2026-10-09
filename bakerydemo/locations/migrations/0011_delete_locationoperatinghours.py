from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("locations", "0010_migrate_operating_hours"),
    ]

    operations = [
        migrations.DeleteModel(
            name="LocationOperatingHours",
        ),
    ]
