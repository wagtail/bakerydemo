

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0008_alter_locationpage_body"),
    ]

    operations = [
        migrations.CreateModel(
            name="LocationWeekDaySlot",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "day",
                    models.CharField(
                        choices=[
                            ("MON", "Monday"),
                            ("TUE", "Tuesday"),
                            ("WED", "Wednesday"),
                            ("THU", "Thursday"),
                            ("FRI", "Friday"),
                            ("SAT", "Saturday"),
                            ("SUN", "Sunday"),
                        ],
                        default="MON",
                        help_text="Select the day of the week",
                        max_length=3,
                    ),
                ),
                (
                    "location",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="week_day_slots",
                        to="locations.locationpage",
                    ),
                ),
            ],
            options={
                "verbose_name": "Week Day Slot",
                "verbose_name_plural": "Week Day Slots",
                "ordering": ["sort_order"],
            },
        ),
        migrations.CreateModel(
            name="LocationHourSlot",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("opening_time", models.TimeField(blank=True, null=True)),
                ("closing_time", models.TimeField(blank=True, null=True)),
                (
                    "closed",
                    models.BooleanField(
                        blank=True,
                        default=False,
                        help_text="Tick if location is closed during this time slot",
                        verbose_name="Closed?",
                    ),
                ),
                (
                    "week_day_slot",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hour_slots",
                        to="locations.locationweekdayslot",
                    ),
                ),
            ],
            options={
                "verbose_name": "Hour Slot",
                "verbose_name_plural": "Hour Slots",
                "ordering": ["sort_order"],
            },
        ),
    ]
