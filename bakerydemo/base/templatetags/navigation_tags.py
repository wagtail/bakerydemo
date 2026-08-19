from django import template
from django.utils.translation import get_language_info
from wagtail.models import Page, Site

from bakerydemo.base.models import FooterText

register = template.Library()


def get_current_page(context):
    return context.get("page") or context.get("self")


def get_page_language_entries(page, request):
    if page is None or not hasattr(page, "locale"):
        return []

    translated_pages = [page, *page.get_translations().live().public()]
    entries_by_code = {}

    for translated_page in translated_pages:
        language_code = translated_page.locale.language_code
        language_info = get_language_info(language_code)

        entries_by_code[language_code] = {
            "code": language_code,
            "name_local": language_info["name_local"],
            "name_translated": language_info["name_translated"],
            "url": request.build_absolute_uri(translated_page.url),
            "is_current": translated_page.pk == page.pk,
        }

    return list(entries_by_code.values())


@register.inclusion_tag("tags/hreflangs.html", takes_context=True)
def hreflangs(context):
    page = get_current_page(context)
    entries = get_page_language_entries(page, context["request"])

    return {
        "translations": [entry for entry in entries if not entry["is_current"]],
    }


@register.inclusion_tag("includes/language_switcher.html", takes_context=True)
def language_switcher(context):
    page = get_current_page(context)
    entries = get_page_language_entries(page, context["request"])

    if len(entries) <= 1:
        return {"render_language_switcher": False}

    current_language = next(entry for entry in entries if entry["is_current"])

    return {
        "render_language_switcher": True,
        "current_language": current_language,
        "languages": entries,
    }


# https://docs.djangoproject.com/en/stable/howto/custom-template-tags/


@register.simple_tag(takes_context=True)
def get_site_root(context):
    # This returns a core.Page. The main menu needs to have the site.root_page
    # defined else will return an object attribute error ('str' object has no
    # attribute 'get_children')
    return Site.find_for_request(context["request"]).root_page


def has_children(page):
    # Generically allow index pages to list their children
    return page.get_children().live().exists()


def is_active(page, current_page):
    # To give us active state on main navigation
    return current_page.url_path.startswith(page.url_path) if current_page else False


# Retrieves the top menu items - the immediate children of the parent page
@register.inclusion_tag("tags/top_menu.html", takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        menuitem.active = (
            calling_page.url_path.startswith(menuitem.url_path)
            if calling_page
            else False
        )
    return {
        "calling_page": calling_page,
        "menuitems": menuitems,
        # required by the pageurl tag that we want to use within this template
        "request": context["request"],
    }


@register.inclusion_tag("tags/breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    self = context.get("self")
    if self is None or self.depth <= 2:
        # When on the home page, displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(self, inclusive=True).filter(depth__gt=1)
    return {
        "ancestors": ancestors,
        "request": context["request"],
    }


@register.inclusion_tag("base/include/footer_text.html", takes_context=True)
def get_footer_text(context):
    # Get the footer text from the context if exists,
    # so that it's possible to pass a custom instance e.g. for previews
    # or page types that need a custom footer
    footer_text = context.get("footer_text", "")

    # If the context doesn't have footer_text defined, get one that's live
    if not footer_text:
        instance = FooterText.objects.filter(live=True).first()
        footer_text = instance.body if instance else ""

    return {
        "footer_text": footer_text,
    }
