from jinja2.ext import Extension

from . import get_video_model

Video = get_video_model()


def video(video, **attrs):
    if isinstance(video, Video):
        defaults = {'preload': True, 'controls': True}
        defaults.update(attrs)
        return video.video_tag(attrs)
    else:
        raise TypeError('Expected type {0}, received {1}.'.format(Video, type(video)))


class WagtailVideosExtension(Extension):

    def __init__(self, environment):
        super(WagtailVideosExtension, self).__init__(environment)

        self.environment.globals.update({
            'video': video,
        })


videos = WagtailVideosExtension
