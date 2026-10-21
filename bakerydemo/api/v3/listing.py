"""
A pages listing endpoint that returns each page's full, type-specific detail.

API v3's ``GET /pages/`` only returns the compact base page schema, with no
equivalent of API v2's ``?fields=`` to include a page type's own fields. A
frontend that renders listings (e.g. cards with images and introductions)
would otherwise have to fetch each page's detail separately.

This endpoint accepts the same filters, ordering, search, and pagination as
``GET /pages/``, but returns the same schema as ``GET /pages/{page_id}/``.
"""

from typing import cast

from django.db.models import Model
from django.http import HttpRequest
from ninja import Query, Router
from ninja.pagination import paginate
from wagtail.api.v3.auth import AllowAnonymous, BearerTokenAuth
from wagtail.api.v3.pagination import WagtailLimitOffsetPagination
from wagtail.api.v3.querysets import get_pages_queryset
from wagtail.api.v3.routers.pages import PageDetailSchema, PageFilterSchema
from wagtail.api.v3.schemas.pages import BASE_PAGE_READ_FIELDS
from wagtail.api.v3.schemas.params import (
    APIFieldFilterSchema,
    OrderingSchema,
    SearchSchema,
)
from wagtail.models import Page

router = Router(tags=["listing"])


class SpecificPages:
    """
    Wrap a page queryset (or search results) so that slicing it returns the
    specific page instances, fetched in one query per page type.
    """

    def __init__(self, queryset):
        self.queryset = queryset

    def __len__(self):
        return self.queryset.count()

    def __getitem__(self, key: slice):
        pages = list(self.queryset[key])
        if self.queryset.model is not Page:
            return pages
        specific = Page.objects.filter(pk__in=[page.pk for page in pages]).specific()
        specific_by_pk = {page.pk: page for page in specific}
        return [specific_by_pk[page.pk] for page in pages]


@router.get(
    "/pages/",
    response=list[PageDetailSchema],
    url_name="listing_pages",
    summary="List pages with their full detail",
    operation_id="listing_pages",
    auth=[BearerTokenAuth(), AllowAnonymous()],
)
@paginate(
    WagtailLimitOffsetPagination,
    pass_parameter="pagination_info",
)
def list_pages(
    request: HttpRequest,
    filters: Query[PageFilterSchema],
    ordering: Query[OrderingSchema],
    search: Query[SearchSchema],
    **kwargs,
):
    # Same as wagtail.api.v3.routers.pages.list_pages
    pagination_info = cast(
        WagtailLimitOffsetPagination.Input,
        kwargs.get("pagination_info"),
    )
    models = cast(list[type[Model]], filters.type)
    model = models[0] if len(models) == 1 else Page
    field_filter = APIFieldFilterSchema.with_exclude_schemas(
        raw_params=request.GET,
        schemas=(PageFilterSchema, OrderingSchema, SearchSchema),
        base_fields=BASE_PAGE_READ_FIELDS,
    )
    queryset = get_pages_queryset(request, model)
    queryset = filters.filter(queryset, request)
    queryset = field_filter.filter_queryset(queryset)
    queryset = ordering.order_queryset(
        queryset,
        pagination_info,
        base_fields=BASE_PAGE_READ_FIELDS,
    )
    queryset = search.search_queryset(request, queryset)

    return SpecificPages(queryset)
