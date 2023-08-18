from distutils.version import LooseVersion

import wagtail
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.views.decorators.http import require_POST
from django.views.decorators.vary import vary_on_headers
from wagtail.search.backends import get_search_backends

from src.wagtailvideos import get_video_model
from src.wagtailvideos.forms import get_video_form
from src.wagtailvideos.permissions import permission_policy

if LooseVersion(wagtail.__version__) >= LooseVersion('2.7'):
    from wagtail.admin.auth import PermissionPolicyChecker
else:
    from wagtail.admin.utils import PermissionPolicyChecker

permission_checker = PermissionPolicyChecker(permission_policy)


def get_video_edit_form(VideoModel):
    VideoForm = get_video_form(VideoModel)

    # Make a new form with the file and focal point fields excluded
    class VideoEditForm(VideoForm):
        class Meta(VideoForm.Meta):
            model = VideoModel
            exclude = (
                'file',
            )

    return VideoEditForm


@vary_on_headers('X-Requested-With')
def add(request):
    Video = get_video_model()
    VideoForm = get_video_form(Video)

    collections = permission_policy.collections_user_has_permission_for(request.user, 'add')
    if len(collections) > 1:
        collections_to_choose = collections
    else:
        # no need to show a collections chooser
        collections_to_choose = None

    if request.method == 'POST':
        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            return HttpResponseBadRequest("Cannot POST to this view without AJAX")

        if not request.FILES:
            return HttpResponseBadRequest("Must upload a file")

        # Build a form for validation
        form = VideoForm({
            'title': request.FILES['files[]'].name,
            'collection': request.POST.get('collection'),
        }, {
            'file': request.FILES['files[]'],
        })
        if form.is_valid():
            # Save
            video = form.save(commit=False)
            video.uploaded_by_user = request.user
            video.save()

            # Success! Send back an edit form
            return JsonResponse({
                'success': True,
                'video_id': int(video.id),
                'form': render_to_string('wagtailvideos/multiple/edit_form.html', {
                    'video': video,
                    'form': get_video_edit_form(Video)(
                        instance=video, prefix='video-%d' % video.id),
                }, request=request),
            })
        else:
            # Validation error
            return JsonResponse({
                'success': False,

                # https://github.com/django/django/blob/stable/1.6.x/django/forms/util.py#L45
                'error_message': '\n'.join(['\n'.join([force_str(i) for i in v]) for k, v in form.errors.items()]),
            })
    else:
        form = VideoForm()

    return render(request, 'wagtailvideos/multiple/add.html', {
        'max_filesize': form.fields['file'].max_upload_size,
        'help_text': form.fields['file'].help_text,
        'error_max_file_size': form.fields['file'].error_messages['file_too_large_unknown_size'],
        'error_accepted_file_types': form.fields['file'].error_messages['invalid_video_format'],
        'collections': collections_to_choose,
    })


@require_POST
def edit(request, video_id, callback=None):
    Video = get_video_model()
    VideoForm = get_video_edit_form(Video)

    video = get_object_or_404(Video, id=video_id)

    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("Cannot POST to this view without AJAX")

    form = VideoForm(
        request.POST, request.FILES, instance=video, prefix='video-' + video_id
    )

    if form.is_valid():
        form.save()

        # Reindex the video to make sure all tags are indexed
        for backend in get_search_backends():
            backend.add(video)

        return JsonResponse({
            'success': True,
            'video_id': int(video_id),
        })
    else:
        return JsonResponse({
            'success': False,
            'video_id': int(video_id),
            'form': render_to_string('wagtailvideos/multiple/edit_form.html', {
                'video': video,
                'form': form,
            }, request=request),
        })


@require_POST
def delete(request, video_id):
    video = get_object_or_404(get_video_model(), id=video_id)

    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("Cannot POST to this view without AJAX")

    video.delete()

    return JsonResponse({
        'success': True,
        'video_id': int(video_id),
    })
