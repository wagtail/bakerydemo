from django.http import HttpRequest
from ninja import Router
from wagtail.api.v3.api import api
from wagtail.api.v3.auth import AllowAnonymous, BearerTokenAuth
from wagtail.api.v3.routers.pages import PageDetailSchema, PageTypeLiteral

from bakerydemo.api.preview import get_preview_page

from .blocks import register_block_schemas
from .listing import router as listing_router

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
    page = get_preview_page(type, token).specific
    if page.id is None:
        # A new page that hasn't been saved yet. The page schemas require an
        # ID, so use a fake one that no page can have. As 0 is falsy, clients
        # can still tell that the page has no real ID.
        page.id = 0
    return page


register_block_schemas()

api.add_router("/preview/", router)
api.add_router("/listing/", listing_router)
