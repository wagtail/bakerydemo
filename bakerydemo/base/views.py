from django.shortcuts import render

from .models import NotFoundPageSettings


def test_404(request):
    settings = NotFoundPageSettings.for_request(request)

    return render(request, "404.html", {"settings": settings})
