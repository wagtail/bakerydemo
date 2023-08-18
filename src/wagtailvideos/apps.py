from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Warning, register

from src.wagtailvideos import ffmpeg


def ffmpeg_check(app_configs, **kwargs):
    messages = []
    if (
        not ffmpeg.installed() and not getattr(settings, 'WAGTAIL_VIDEOS_DISABLE_TRANSCODE', False)
    ):
        messages.append(
            Warning(
                'ffmpeg could not be found on your system. Transcoding will be disabled',
                hint=None,
                id='wagtailvideos.W001',
            )
        )
    return messages


class WagtailVideosApp(AppConfig):
    name = 'src.wagtailvideos'
    label = 'wagtailvideos'
    verbose_name = 'Wagtail Videos'

    def ready(self):
        from src.wagtailvideos.signals import register_signal_handlers
        register_signal_handlers()
        register(ffmpeg_check)
