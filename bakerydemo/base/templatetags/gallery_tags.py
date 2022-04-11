from django import template

from wagtail.images import get_image_model

register = template.Library()


# Retrieves a single gallery item and returns a gallery of images
@register.inclusion_tag('tags/gallery.html', takes_context=True)
def gallery(context, gallery):
    images = get_image_model().objects.filter(collection=gallery)

    return {
        'images': images,
        'request': context['request'],
    }
