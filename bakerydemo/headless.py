from wagtail_headless_preview.models import HeadlessMixin


class CustomHeadlessMixin(HeadlessMixin):
    def get_client_root_url(self, request):
        """
        Use a dedicated API endpoint for drafts.
        By default, the method uses the root URL of the client site.
        """
        root_url = super().get_client_root_url(request)
        if getattr(request, "is_preview", False):
            return f"{root_url}/api/draft"
        return root_url
