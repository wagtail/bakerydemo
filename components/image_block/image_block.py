from django_components import component
from components.image_block import block_name, template_name, css_name, js_name


@component.register(block_name)
class ImageBlockComponent(component.Component):
    """ImageBlockComponent component."""

    template_name = template_name

    class Media:
        css = css_name
        js = js_name
