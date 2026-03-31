from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Case, When
from django.shortcuts import render
from wagtail.contrib.search_promotions.models import Query
from wagtail.models import Page

from bakerydemo.blog.models import BlogPage
from bakerydemo.breads.models import BreadPage
from bakerydemo.locations.models import LocationPage
from bakerydemo.recipes.models import (
    RecipePage,  # fixed typo: bakerydemo not backerydemo
)


def search(request):
    search_query = request.GET.get("q", None)
    if search_query:
        if "elasticsearch" in settings.WAGTAILSEARCH_BACKENDS["default"]["BACKEND"]:
            search_results = Page.objects.live().search(search_query)
        else:
            blog_results = BlogPage.objects.live().search(search_query)
            blog_page_ids = [p.page_ptr.id for p in blog_results]

            bread_results = BreadPage.objects.live().search(search_query)
            bread_page_ids = [p.page_ptr.id for p in bread_results]

            location_results = LocationPage.objects.live().search(search_query)
            location_result_ids = [p.page_ptr.id for p in location_results]

            recipe_results = RecipePage.objects.live().search(search_query)  # added
            recipe_page_ids = [p.page_ptr.id for p in recipe_results]  # added

            page_ids = (
                blog_page_ids + bread_page_ids + location_result_ids + recipe_page_ids
            )  # added recipe_page_ids

            preserved_order = Case(
                *[When(id=pk, then=pos) for pos, pk in enumerate(page_ids)]
            )
            search_results = (
                Page.objects.live().filter(id__in=page_ids).order_by(preserved_order)
            )

        query = Query.get(search_query)
        query.add_hit()
    else:
        search_results = Page.objects.none()

    page = request.GET.get("page", 1)
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(
        request,
        "search/search_results.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )
