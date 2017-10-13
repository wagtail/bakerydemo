from django.conf import settings


def global_settings(request):
    # Add below any settings needed from the templates
    return {
        'ENABLE_USER_BAR': settings.ENABLE_USER_BAR,
    }
