import re

from django.conf import settings
from django.http import Http404
from django.shortcuts import reverse
from django.forms import CharField, BooleanField
from django.utils.translation import gettext_lazy as _
from django.forms import Form
from wagtail.admin.forms.choosers import URLOrAbsolutePathField
from wagtail.admin.auth import PermissionPolicyChecker
from wagtail.admin.views.chooser import LINK_CONVERSION_ALL, LINK_CONVERSION_EXACT, LINK_CONVERSION_CONFIRM, \
    shared_context
from wagtail.models import Site
from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.images.permissions import permission_policy


permission_checker = PermissionPolicyChecker(permission_policy)


class ExtendedExternalLinkChooserForm(Form):
    url = URLOrAbsolutePathField(required=True, label=_("URL"))
    link_text = CharField(required=False, label='Текст ссылки')
    target = BooleanField(required=False, label='Открывать в новом окне', initial=False)
    rel = BooleanField(required=False, label='Без индексирования', initial=False)
    download = BooleanField(required=False, label='Ссылка на скачивание', initial=False)


"""
Wagtail does not support customizing link. And authors oppose this:
https://github.com/wagtail/wagtail/pull/2223#issuecomment-182788315
Using middleware i intercept each request and if it is equal to '/admin/choose-external-link/', replace view.
patched_external_link duplicates original view, but uses extended form. And provide additional keys in initial data.
Nothing else changed
"""


def patched_external_link(request):
    initial_data = {
        'url': request.GET.get('link_url', ''),
        'link_text': request.GET.get('link_text', ''),
        'rel': request.GET.get('rel', False),
        'target': request.GET.get('target', False),
        'download': request.GET.get('download', False)
    }

    if request.method == 'POST':
        form = ExtendedExternalLinkChooserForm(request.POST, initial=request.POST, prefix='external-link-chooser')

        if form.is_valid():
            submitted_url = form.cleaned_data['url']
            result = {
                'url': submitted_url,
                'title': form.cleaned_data['link_text'].strip() or form.cleaned_data['url'],
                # If the user has explicitly entered / edited something in the link_text field,
                # always use that text. If not, we should favour keeping the existing link/selection
                # text, where applicable.
                # (Normally this will match the link_text passed in the URL here anyhow,
                # but that won't account for non-text content such as images.)
                'prefer_this_title_as_link_text': ('link_text' in form.changed_data),
                'rel': form.cleaned_data['rel'],
                'target': form.cleaned_data['target'],
                'download': form.cleaned_data['download'],
            }

            link_conversion = getattr(settings, 'WAGTAILADMIN_EXTERNAL_LINK_CONVERSION', LINK_CONVERSION_ALL).lower()

            if link_conversion not in [LINK_CONVERSION_ALL, LINK_CONVERSION_EXACT, LINK_CONVERSION_CONFIRM]:
                # We should not attempt to convert external urls to page links
                return render_modal_workflow(
                    request, None, None,
                    None, json_data={'step': 'external_link_chosen', 'result': result}
                )

            # Next, we should check if the url matches an internal page
            # Strip the url of its query/fragment link parameters - these won't match a page
            url_without_query = re.split(r"\?|#", submitted_url)[0]

            # Start by finding any sites the url could potentially match
            sites = getattr(request, '_wagtail_cached_site_root_paths', None)
            if sites is None:
                sites = Site.get_site_root_paths()

            match_relative_paths = submitted_url.startswith('/') and len(sites) == 1
            # We should only match relative urls if there's only a single site
            # Otherwise this could get very annoying accidentally matching coincidentally
            # named pages on different sites

            if match_relative_paths:
                possible_sites = [
                    (pk, url_without_query)
                    for pk, path, url, language_code
                    in sites
                ]
            else:
                possible_sites = [
                    (pk, url_without_query[len(url):])
                    for pk, path, url, language_code
                    in sites
                    if submitted_url.startswith(url)
                ]

            # Loop over possible sites to identify a page match
            for pk, url in possible_sites:
                try:
                    route = Site.objects.get(pk=pk).root_page.specific.route(
                        request,
                        [component for component in url.split('/') if component]
                    )

                    matched_page = route.page.specific

                    internal_data = {
                        'id': matched_page.pk,
                        'parentId': matched_page.get_parent().pk,
                        'adminTitle': matched_page.draft_title,
                        'editUrl': reverse('wagtailadmin_pages:edit', args=(matched_page.pk,)),
                        'url': matched_page.url
                    }

                    # Let's check what this page's normal url would be
                    normal_url = matched_page.get_url_parts(request=request)[-1] if match_relative_paths else matched_page.get_full_url(request=request)

                    # If that's what the user provided, great. Let's just convert the external
                    # url to an internal link automatically unless we're set up tp manually check
                    # all conversions
                    if normal_url == submitted_url and link_conversion != LINK_CONVERSION_CONFIRM:
                        return render_modal_workflow(
                            request,
                            None,
                            None,
                            None,
                            json_data={'step': 'external_link_chosen', 'result': internal_data}
                        )
                    # If not, they might lose query parameters or routable page information

                    if link_conversion == LINK_CONVERSION_EXACT:
                        # We should only convert exact matches
                        continue

                    # Let's confirm the conversion with them explicitly
                    else:
                        return render_modal_workflow(
                            request,
                            'wagtailadmin/chooser/confirm_external_to_internal.html',
                            None,
                            {
                                'submitted_url': submitted_url,
                                'internal_url': normal_url,
                                'page': matched_page.draft_title,
                            },
                            json_data={'step': 'confirm_external_to_internal', 'external': result, 'internal': internal_data}
                        )

                except Http404:
                    continue

            # Otherwise, with no internal matches, fall back to an external url
            return render_modal_workflow(
                request, None, None,
                None, json_data={'step': 'external_link_chosen', 'result': result}
            )
    else:
        form = ExtendedExternalLinkChooserForm(initial=initial_data, prefix='external-link-chooser')

    return render_modal_workflow(
        request,
        'wagtailadmin/chooser/external_link.html', None,
        shared_context(request, {
            'form': form,
        }), json_data={'step': 'external_link'}
    )
