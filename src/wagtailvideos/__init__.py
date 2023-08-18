from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

default_app_config = 'wagtailvideos.apps.WagtailVideosApp'


def is_modeladmin_installed():
    from django.apps import apps
    return apps.is_installed('wagtail.contrib.modeladmin')


def get_video_model_string():
    return getattr(settings, 'WAGTAILVIDEOS_VIDEO_MODEL', 'wagtailvideos.Video')


def get_video_model():
    from django.apps import apps
    model_string = get_video_model_string()
    try:
        return apps.get_model(model_string)
    except ValueError:
        raise ImproperlyConfigured("WAGTAILVIDEOS_VIDEO_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "WAGTAILVIDEOS_VIDEO_MODEL refers to model '%s' that has not been installed" % model_string
        )
