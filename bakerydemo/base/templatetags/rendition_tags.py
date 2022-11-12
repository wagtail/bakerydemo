from django import template

register = template.Library()


@register.inclusion_tag("tags/renditions.html")
def renditions(image, *specs: str):
    return {"renditions": image.get_renditions(*specs)}
