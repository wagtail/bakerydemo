from wagtail.images.models import Image


# Retrieves a single gallery item and returns a gallery of images
def gallery(gallery):
    images = Image.objects.filter(collection=gallery)

    return {
        "images": images,
    }
