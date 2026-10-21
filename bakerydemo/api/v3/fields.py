from typing import TypedDict

from wagtail.api.v3.fields import FieldSerializer


class PageLinkMeta(TypedDict):
    type: str
    html_url: str | None


class PageLink(TypedDict):
    id: int
    title: str
    meta: PageLinkMeta


class PageLinkField(FieldSerializer):
    """
    Serialize a ForeignKey to a page as a lightweight link.

    By default, API v3 expands a page ForeignKey using the target model's
    ``api_fields``, without the page's ``title`` or URL (and without its ``id``
    for page subclasses). That's not useful for rendering a link, so use this
    to output the same shape as ``meta.parent``.
    """

    def to_representation(self, value) -> PageLink:
        return PageLink(
            id=value.pk,
            title=value.title,
            meta=PageLinkMeta(
                type=value.specific_class._meta.label,
                html_url=value.get_full_url(),
            ),
        )
