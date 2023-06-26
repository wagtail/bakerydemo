from wagtail.images.apps import WagtailImagesAppConfig

# The CustomImagesAppConfig class sets a custom attribute default_attrs which specifies additional default attributes
# to be added to all images in the project. In this case, the default attributes are "decoding": "async" and
# "loading": "lazy", which can enhance the loading and decoding behavior of the images.


class CustomImagesAppConfig(WagtailImagesAppConfig):
    default_attrs = {"decoding": "async", "loading": "lazy"}
