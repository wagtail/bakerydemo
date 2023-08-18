import json

from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.admin.staticfiles import versioned_static
from wagtail.admin.widgets import BaseChooser, BaseChooserAdapter
from wagtail.telepath import register

from src.wagtailvideos import get_video_model


class AdminVideoChooser(BaseChooser):
    choose_one_text = _('Choose a video')
    template_name = "wagtailvideos/widgets/video_chooser.html"
    chooser_modal_url_name = "wagtailvideos_chooser:choose"
    icon = "media"
    classname = "image-chooser"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = get_video_model()

    def get_value_data_from_instance(self, instance):
        data = super().get_value_data_from_instance(instance)
        data["preview"] = {
            "url": instance.thumbnail.url if instance.thumbnail else "",
            "width": 165,
            "height": 165,
        }
        return data

    def get_context(self, name, value_data, attrs):
        context = super().get_context(name, value_data, attrs)
        context["preview"] = value_data.get("preview", {})
        return context

    def render_js_init(self, id_, name, value_data):
        return "new VideoChooser({0});".format(json.dumps(id_))

    @property
    def media(self):
        return forms.Media(
            js=[
                versioned_static("wagtailimages/js/image-chooser-modal.js"),
                versioned_static("wagtailimages/js/image-chooser.js"),
                versioned_static("wagtailvideos/js/video-chooser.js"),
            ]
        )


class VideoChooserAdapter(BaseChooserAdapter):
    js_constructor = "wagtailvideos.widgets.VideoChooser"

    @cached_property
    def media(self):
        return forms.Media(
            js=[
                versioned_static("wagtailimages/js/image-chooser-telepath.js"),
                versioned_static("wagtailvideos/js/video-chooser-telepath.js"),
            ]
        )


register(VideoChooserAdapter(), AdminVideoChooser)
