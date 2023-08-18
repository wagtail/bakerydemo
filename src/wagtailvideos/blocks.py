from django.utils.functional import cached_property
from wagtail.blocks import ChooserBlock


class VideoChooserBlock(ChooserBlock):
    @cached_property
    def target_model(self):
        from src.wagtailvideos import get_video_model
        return get_video_model()

    @cached_property
    def widget(self):
        from src.wagtailvideos.widgets import AdminVideoChooser
        return AdminVideoChooser()

    def render_basic(self, value, context=None):
        if value:
            return value.video_tag(attrs={"controls": True})
        else:
            return ""

    class Meta:
        icon = 'media'
