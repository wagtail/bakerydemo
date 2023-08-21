from wagtail.admin.panels import FieldPanel

from .widgets import AdminVideoChooser


class VideoChooserPanel(FieldPanel):

    def __init__(self, field_name, disable_comments=None, permission=None, **kwargs):
        kwargs['widget'] = AdminVideoChooser
        super().__init__(field_name, disable_comments=disable_comments, permission=permission, **kwargs)
