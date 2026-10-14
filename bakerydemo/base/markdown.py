from django.http import HttpResponse


class MarkdownPageMixin:
    """
    Serves pages as Markdown to clients that request it with an
    `Accept: text/markdown` header, and as HTML otherwise.

    The Markdown is converted from the page's rendered HTML template, so it
    matches what visitors see, without a separate Markdown template.
    """

    response_media_types = ["text/html", "text/markdown"]

    def get_response_media_type(self, request):
        # Demo only: ?format=md shows the Markdown in a browser, which can't
        # easily send an Accept: text/markdown header.
        if request.GET.get("format") == "md":
            return "text/markdown"
        return super().get_response_media_type(request)

    def serve(self, request, *args, **kwargs):
        response = super().serve(request, *args, **kwargs)
        if self.get_response_media_type(request) != "text/markdown":
            return response

        # Imported here, as wagtail.admin.rich_text imports page models.
        from wagtail.admin.rich_text.converters.html_markdown import (
            HTMLToMarkdownConverter,
        )

        # Page responses are TemplateResponses, rendered lazily.
        if hasattr(response, "render"):
            response.render()
        # Leave redirects, errors and non-HTML responses as they are.
        if response.status_code != 200 or "text/html" not in response.get(
            "Content-Type", ""
        ):
            return response

        converter = HTMLToMarkdownConverter(base_url=self.get_full_url(request))
        markdown = converter.convert(response.content.decode(response.charset))
        return HttpResponse(markdown, content_type="text/markdown; charset=utf-8")
