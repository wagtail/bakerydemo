from django.views.generic import TemplateView
from wagtail.admin.userbar import (
    AccessibilityItem,
    AddPageItem,
    AdminItem,
    EditPageItem,
    ExplorePageItem,
    apply_userbar_hooks,
)
from wagtail.models import Page, Revision
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


def get_userbar_context(request, object, position):
    # Extracted from wagtail.admin.templatetags.wagtailuserbar.wagtailuserbar

    revision_id = getattr(request, "revision_id", None)
    in_preview_panel = getattr(request, "in_preview_panel", False)

    if in_preview_panel:
        items = []
    else:
        items = [AdminItem()]

    if isinstance(object, Page) and object.pk:
        if revision_id:
            revision = (
                Revision.objects.for_instance(object)
                .filter(id=revision_id)
                .prefetch_related("content_object")
                .first()
            )
            revision_object = revision.content_object if revision else None
            items.append(ExplorePageItem(revision_object))
            items.append(EditPageItem(revision_object))
        else:
            # Not a revision
            items.append(ExplorePageItem(object))
            items.append(EditPageItem(object))
            items.append(AddPageItem(object))

    items.append(AccessibilityItem())

    apply_userbar_hooks(request, items, object)

    # Render the items
    rendered_items = [item.render(request) for item in items]

    # Remove any unrendered items
    rendered_items = [item for item in rendered_items if item]

    # Render the userbar items
    return {
        "request": request,
        "items": rendered_items,
        "position": position,
        "page": object,
        "revision_id": revision_id,
    }


class UserbarView(TemplateView):
    template_name = "wagtailadmin/userbar/base.html"
    http_method_names = ["get"]

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        client_url = headless_preview_settings.CLIENT_URLS["default"]
        response["Access-Control-Allow-Origin"] = client_url
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_userbar_context(self.request, None, None))
        return context
