from django.template.context_processors import csrf
from django.template.defaultfilters import (
    cut,
    date,
    linebreaks,
    pluralize,
    slugify,
    truncatewords,
    urlencode,
)
from django.contrib.staticfiles.storage import staticfiles_storage
from jinja2 import pass_context
from jinja2.ext import Extension

from wagtail.contrib.search_promotions.templatetags.wagtailsearchpromotions_tags import (
    get_search_promotions,
)

from bakerydemo.base.templatetags.navigation_tags import (
    breadcrumbs,
    get_footer_text,
    get_site_root,
    top_menu,
    top_menu_children,
)
from bakerydemo.base.templatetags.gallery_tags import gallery


class BaseExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        self.environment.globals.update(
            {
                "static": staticfiles_storage.url,
                "csrf": csrf,
                "get_search_promotions": get_search_promotions,
                "breadcrumbs": pass_context(breadcrumbs),
                "get_footer_text": pass_context(get_footer_text),
                "get_site_root": pass_context(get_site_root),
                "top_menu": top_menu,
                "top_menu_children": top_menu_children,
                "gallery": gallery,
            }
        )

        self.environment.filters.update(
            {
                "cut": cut,
                "date": date,
                "linebreaks": linebreaks,
                "pluralize": pluralize,
                "slugify": slugify,
                "truncatewords": truncatewords,
                "urlencode": urlencode,
            }
        )


base = BaseExtension
