from django import template
from wagtail.models import Page, Site

from bakerydemo.base.models import FooterMenu, FooterText, MainMenu

register = template.Library()
# https://docs.djangoproject.com/en/stable/howto/custom-template-tags/


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context["request"]).root_page


@register.inclusion_tag("base/include/main_menu.html", takes_context=True)
def get_main_menu(context):
    main_menu = context.get("main_menu", None)

    if not main_menu:
        instance = MainMenu.objects.filter(live=True).first()
        main_menu = instance if instance else None

    calling_page = context.get("self", None)

    return {
        "main_menu": main_menu,
        "calling_page": calling_page,
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


@register.inclusion_tag("base/include/footer_menu.html", takes_context=True)
def get_footer_menu(context):
    footer_menu = context.get("footer_menu", None)

    if not footer_menu:
        instance = FooterMenu.objects.filter(live=True).first()
        footer_menu = instance if instance else None

    return {
        "footer_menu": footer_menu,
    }
