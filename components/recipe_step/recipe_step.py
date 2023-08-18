from django_components import component
from components.recipe_step import block_name, template_name, css_name, js_name


@component.register(block_name)
class Component(component.Component):
    """Component."""

    template_name = template_name

    class Media:
        css = css_name
        js = js_name
