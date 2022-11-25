from django.conf import settings


def settings_injector(request):
    return {
        "DEFAULT_ADMIN_PASSWORD": settings.DEFAULT_ADMIN_PASSWORD,
        "DEFAULT_ADMIN_USERNAME": settings.DEFAULT_ADMIN_USERNAME,
        "SHOW_DEMO_BANNER": settings.SHOW_DEMO_BANNER,
    }
