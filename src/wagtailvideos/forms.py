from django import forms
from django.forms.models import modelform_factory
from django.utils.translation import gettext as _
from enumchoicefield.forms import EnumField
from wagtail.admin import widgets
from wagtail.admin.forms.collections import (
    BaseCollectionMemberForm, collection_member_permission_formset_factory)

from src.wagtailvideos.fields import WagtailVideoField
from src.wagtailvideos.models import MediaFormats, Video, VideoQuality
from src.wagtailvideos.permissions import \
    permission_policy as video_permission_policy


class BaseVideoForm(BaseCollectionMemberForm):
    permission_policy = video_permission_policy

    def __init__(self, *args, **kwargs):
        super(BaseVideoForm, self).__init__(*args, **kwargs)
        # A file is only required if there is not already a file, such as when
        # editing an existing video.  The file field is not used on the
        # multiple-upload forms, so may not be present
        if 'file' in self.fields:
            self.fields['file'].required = 'file' not in self.initial or not self.initial['file']


# Callback to allow us to override the default form field for the video file field
def formfield_for_dbfield(db_field, **kwargs):
    # Check if this is the file field
    if db_field.name == 'file':
        return WagtailVideoField(**kwargs)

    # For all other fields, just call its formfield() method.
    return db_field.formfield(**kwargs)


def get_video_form(model):
    fields = model.admin_form_fields
    if 'collection' not in fields:
        # force addition of the 'collection' field, because leaving it out can
        # cause dubious results when multiple collections exist (e.g adding the
        # document to the root collection where the user may not have permission) -
        # and when only one collection exists, it will get hidden anyway.
        fields = list(fields) + ['collection']

    return modelform_factory(
        model,
        form=BaseVideoForm,
        fields=fields,
        formfield_callback=formfield_for_dbfield,
        # set the 'file' widget to a FileInput rather than the default ClearableFileInput
        # so that when editing, we don't get the 'currently: ...' banner which is
        # a bit pointless here
        widgets={
            'tags': widgets.AdminTagWidget,
            'file': forms.FileInput(),
            'thumbnail': forms.FileInput(),
        })


class VideoTranscodeAdminForm(forms.Form):
    media_format = EnumField(MediaFormats)
    quality = EnumField(VideoQuality)

    def __init__(self, video, data=None, **kwargs):
        super(VideoTranscodeAdminForm, self).__init__(data=data, **kwargs)
        self.video = video

    def save(self):
        media_format = self.cleaned_data['media_format']
        quality = self.cleaned_data['quality']
        self.video.do_transcode(media_format, quality)


GroupVideoPermissionFormSet = collection_member_permission_formset_factory(
    Video,
    [
        ('add_video', _("Add"), _("Add/edit videos you own")),
        ('change_video', _("Edit"), _("Edit any video")),
        ('choose_video', _("Choose"), _("Choose video")),
    ],
    'wagtailvideos/permissions/includes/video_permissions_formset.html'
)
