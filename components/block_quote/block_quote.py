"""Component."""
from django_components import component


@component.register("block_quote")
class Comment(component.Component):
    """Comment component."""

    template_name = "block_quote/block_quote.html"

    class Media:
        css = "block_quote/block_quote.css"
        js = "block_quote/block_quote.js"
