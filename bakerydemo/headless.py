from django.http import HttpRequest
from django.utils.http import urlencode
from django.views.generic import TemplateView
from wagtail.admin.userbar import (
    Userbar,
)
from wagtail_headless_preview.models import HeadlessMixin
from wagtail_headless_preview.settings import headless_preview_settings


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

    def get_preview_url(self, request: HttpRequest, token: str) -> str:
        return (
            self.get_client_root_url(request)
            + "?"
            + urlencode(
                {
                    "content_type": self.get_content_type_str(),
                    "token": token,
                    "in_preview_panel": getattr(request, "in_preview_panel", False),
                }
            )
        )


class UserbarView(TemplateView):
    template_name = Userbar.template_name
    http_method_names = ["get"]

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        client_url = headless_preview_settings.CLIENT_URLS["default"]
        response["Access-Control-Allow-Origin"] = client_url
        return response

    def get_context_data(self, **kwargs):
        return Userbar(object=None, position="bottom-left").get_context_data(
            super().get_context_data(request=self.request, **kwargs)
        )
