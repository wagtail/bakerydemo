from django_components import component

from components.heading_block import block_name, template_name, css_name, js_name


@component.register(block_name)
class HeadingComponent(component.Component):
    """HeadingComponent component."""

    template_name = template_name

    class Media:
        css = css_name
        js = js_name
