from django import template
from taggit.models import Tag
from wagtail.images.models import Image

register = template.Library()


# Retrieves a single gallery item and returns a gallery of images
# and their tags
@register.inclusion_tag("tags/gallery.html", takes_context=True)
def gallery(context, gallery):
    images = Image.objects.filter(collection=gallery)
    ids = [k.id for k in images]
    tags = list(
        Tag.objects.filter(taggit_taggeditem_items__object_id__in=ids).distinct()
    )
    return {
        "tags": tags,
        "images": images,
        "request": context["request"],
    }
