from django_filters import DateFromToRangeFilter, FilterSet
from wagtail.admin.filters import DateRangePickerWidget


class RevisionFilterSetMixin(FilterSet):
    latest_revision_created_at = DateFromToRangeFilter(
        field_name="latest_revision__created_at",
        label="Date updated",
        widget=DateRangePickerWidget,
    )
