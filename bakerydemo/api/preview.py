from django.contrib.contenttypes.models import ContentType
from wagtail_headless_preview.models import PagePreview


def get_preview_page(content_type: str, token: str):
    app_label, model = content_type.split(".")
    content_type = ContentType.objects.get_by_natural_key(app_label, model.lower())

    page_preview = PagePreview.objects.get(content_type=content_type, token=token)
    return page_preview.as_page()
