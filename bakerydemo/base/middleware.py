import re

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.template.loader import render_to_string


class DemoBannerMiddleware:
    """
    When bakerydemo is being run as the Wagtail Demo, show a banner at the top
    of the page mentioning when the site will be reset.
    """

    insert_after_re = re.compile(r"<body .*?>", flags=re.IGNORECASE)

    def __init__(self, get_response):
        if not settings.SHOW_DEMO_BANNER:
            raise MiddlewareNotUsed()

        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.maybe_inject(response)
        return response

    def maybe_inject(self, response):
        # https://github.com/adamchainz/django-browser-reload/blob/main/src/django_browser_reload/middleware.py#L61
        if (
            getattr(response, "streaming", False)
            or response.get("Content-Encoding", "")
            or response.get("Content-Type", "").split(";", 1)[0] != "text/html"
        ):
            return

        content = response.content.decode(response.charset)

        try:
            match = next(self.insert_after_re.finditer(content))
        except StopIteration:
            return

        head = content[: match.start()]
        tag = match[0]
        tail = content[match.end() :]

        response.content = (
            head + tag + render_to_string("base/demo_banner.html", {}) + tail
        )
        if "Content-Length" in response:
            response["Content-Length"] = len(response.content)
