import uuid

from django.core.management.color import no_style
from django.db import migrations

# A fixed namespace so the time slots created from the old hours get stable
# UUIDs, which keeps the migrated rows and revision content in sync.
UUID_NAMESPACE = uuid.UUID("5d2c1a9e-7b3f-4e8a-9c1d-6f0b2a4e8d73")


def time_slot_uuid(old_pk, index=0):
    return uuid.uuid5(UUID_NAMESPACE, f"locationoperatinghours-{old_pk}-{index}")


def convert_serialized_hours(old_hours):
    """
    Convert the serialized hours_of_operation data stored in a revision from
    one flat slot per row to a day with nested time slots. Days keep the
    primary key of the row they were created from.
    """
    new_hours = []
    for old in old_hours:
        time_slots = []
        if (
            not old.get("closed")
            and old.get("opening_time")
            and old.get("closing_time")
        ):
            time_slots.append(
                {
                    "pk": str(time_slot_uuid(old["pk"])),
                    "sort_order": 0,
                    "opening_time": old["opening_time"],
                    "closing_time": old["closing_time"],
                    "day": old["pk"],
                }
            )
        new_hours.append(
            {
                "pk": old["pk"],
                "sort_order": old.get("sort_order"),
                "day": old["day"],
                "closed": bool(old.get("closed")),
                "location": old.get("location"),
                "time_slots": time_slots,
            }
        )
    return new_hours


def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    OldHours = apps.get_model("locations", "LocationOperatingHours")
    Day = apps.get_model("locations", "LocationOperatingDay")
    TimeSlot = apps.get_model("locations", "LocationOperatingTimeSlot")
    ContentType = apps.get_model("contenttypes", "ContentType")
    Revision = apps.get_model("wagtailcore", "Revision")

    for old in OldHours.objects.using(db_alias).all():
        day = Day.objects.using(db_alias).create(
            pk=old.pk,
            location_id=old.location_id,
            sort_order=old.sort_order,
            day=old.day,
            closed=bool(old.closed),
        )
        if not old.closed and old.opening_time and old.closing_time:
            TimeSlot.objects.using(db_alias).create(
                uuid=time_slot_uuid(old.pk),
                day=day,
                sort_order=0,
                opening_time=old.opening_time,
                closing_time=old.closing_time,
            )

    # The days were created with explicit primary keys, so make sure the
    # database's sequence (if any) continues after them.
    sequence_sql = schema_editor.connection.ops.sequence_reset_sql(no_style(), [Day])
    with schema_editor.connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)

    # Update existing revisions so that the hours are not lost when editing
    # a page whose latest revision predates this migration.
    content_type = ContentType.objects.using(db_alias).filter(
        app_label="locations", model="locationpage"
    )
    revisions = Revision.objects.using(db_alias).filter(content_type__in=content_type)
    for revision in revisions.iterator():
        content = revision.content
        if "hours_of_operation" not in content:
            continue
        content["hours_of_operation"] = convert_serialized_hours(
            content["hours_of_operation"]
        )
        revision.content = content
        revision.save(update_fields=["content"])


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("locations", "0009_locationoperatingday_locationoperatingtimeslot"),
        ("wagtailcore", "0070_rename_pagerevision_revision"),
    ]

    operations = [
        migrations.RunPython(forwards_func, migrations.RunPython.noop),
    ]
