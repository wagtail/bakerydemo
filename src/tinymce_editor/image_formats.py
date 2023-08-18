from wagtail.images.formats import Format, unregister_image_format, register_image_format
from django.utils.html import escape
from django.utils.safestring import mark_safe


class DefaultImageFormat(Format):
    def editor_attributes(self, image, alt_text):
        # need to add contenteditable=false to prevent editing within the embed
        original_attrs = super(DefaultImageFormat, self).editor_attributes(image, alt_text)
        original_attrs['contenteditable'] = 'false'
        return original_attrs

    def image_to_html(self, image, alt_text, extra_attributes=None):
        if image.filename.split('.')[-1] == 'gif':
            jpeg_rendition = image.get_rendition('max-680x500')
            webp_rendition = None
        else:
            jpeg_rendition = image.get_rendition('format-jpeg')
            webp_rendition = image.get_rendition('format-webp')

        image_tag = """
                    <img src="{}" alt="{}" loading="lazy" class="_img_resp">
                    """.format(getattr(webp_rendition, 'full_url', ''),
                               jpeg_rendition.full_url,
                               alt_text)

        return mark_safe(image_tag)


unregister_image_format('fullwidth')
unregister_image_format('left')
unregister_image_format('right')


register_image_format(
    DefaultImageFormat('Default', 'Default image', '', 'format-jpeg')
)
