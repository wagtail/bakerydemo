from rest_framework.fields import CharField
from wagtail.rich_text import expand_db_html


class RichTextSerializer(CharField):
    def to_representation(self, instance):
        return expand_db_html(super().to_representation(instance))
