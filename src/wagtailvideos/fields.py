from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms.fields import FileField
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _


class WagtailVideoField(FileField):
    def __init__(self, *args, **kwargs):
        super(WagtailVideoField, self).__init__(*args, **kwargs)

        # Get max upload size from settings
        self.max_upload_size = getattr(settings, 'WAGTAILVIDEOS_MAX_UPLOAD_SIZE', 1024 * 1024 * 1024)
        max_upload_size_text = filesizeformat(self.max_upload_size)

        # Help text
        if self.max_upload_size is not None:
            self.help_text = _(
                "Maximum filesize: %(max_upload_size)s."
            ) % {
                'max_upload_size': max_upload_size_text,
            }

        # Error messages
        self.error_messages['invalid_video_format'] = _(
            "Not a valid video. Content type was %s."
        )

        self.error_messages['file_too_large'] = _(
            "This file is too big (%%s). Maximum filesize %s."
        ) % max_upload_size_text

        self.error_messages['file_too_large_unknown_size'] = _(
            "This file is too big. Maximum filesize %s."
        ) % max_upload_size_text

    def check_video_file_format(self, f):
        if not f.content_type.startswith('video'):
            raise ValidationError(self.error_messages['invalid_video_format'] % f.content_type)

    def check_video_file_size(self, f):
        # Upload size checking can be disabled by setting max upload size to None
        if self.max_upload_size is None:
            return

        # Check the filesize
        if f.size > self.max_upload_size:
            raise ValidationError(self.error_messages['file_too_large'] % (
                filesizeformat(f.size),
            ), code='file_too_large')

    def to_python(self, data):
        f = super(WagtailVideoField, self).to_python(data)

        if f is not None:
            self.check_video_file_size(f)
            self.check_video_file_format(f)

        return f
