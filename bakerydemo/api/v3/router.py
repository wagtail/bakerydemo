from django.http import HttpRequest
from ninja import Router
from wagtail.api.v3.api import api
from wagtail.api.v3.auth import AllowAnonymous, BearerTokenAuth
from wagtail.api.v3.routers.pages import PageDetailSchema, PageTypeLiteral

from bakerydemo.api.preview import get_preview_page

router = Router(tags=["preview"])


@router.get(
    "/",
    response=PageDetailSchema,
    url_name="detail_preview",
    summary="Page preview detail",
    operation_id="preview_detail",
    auth=[BearerTokenAuth(), AllowAnonymous()],
)
def get_preview(request: HttpRequest, type: PageTypeLiteral, token: str):
    return get_preview_page(type, token).specific


api.add_router("/preview/", router)
