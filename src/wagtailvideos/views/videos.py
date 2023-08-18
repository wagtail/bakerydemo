from distutils.version import LooseVersion

import wagtail
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.decorators.vary import vary_on_headers
from wagtail.admin import messages
from wagtail.admin.forms.search import SearchForm
from wagtail.contrib.modeladmin.helpers import AdminURLHelper
from wagtail.models import Collection
from wagtail.search.backends import get_search_backends

from src.wagtailvideos import ffmpeg, get_video_model, is_modeladmin_installed
from src.wagtailvideos.forms import VideoTranscodeAdminForm, get_video_form
from src.wagtailvideos.permissions import permission_policy

if LooseVersion(wagtail.__version__) >= LooseVersion('2.7'):
    from wagtail.admin.auth import PermissionPolicyChecker
    from wagtail.admin.models import popular_tags_for_model
else:
    from wagtail.admin.utils import (
        PermissionPolicyChecker, popular_tags_for_model)

permission_checker = PermissionPolicyChecker(permission_policy)


@permission_checker.require_any('add', 'change', 'delete', 'choose')
@vary_on_headers('X-Requested-With')
def index(request):
    # Get Videos (filtered by user permission)
    Video = get_video_model()

    collections = permission_policy.collections_user_has_any_permission_for(
        request.user, ['add', 'change', 'delete', 'choose'])
    if len(collections) > 1:
        collections_to_choose = collections
    else:
        # no need to show a collections chooser
        collections_to_choose = None

    videos = Video.objects.filter(collection__in=collections)

    # Search
    query_string = None
    if 'q' in request.GET:
        form = SearchForm(request.GET, placeholder=_("Search videos"))
        if form.is_valid():
            query_string = form.cleaned_data['q']

            videos = videos.search(query_string)
    else:
        form = SearchForm(placeholder=_("Search videos"))

    # Filter by collection
    current_collection = None
    collection_id = request.GET.get('collection_id')
    if collection_id:
        try:
            current_collection = Collection.objects.get(id=collection_id)
            videos = videos.filter(collection=current_collection)
        except (ValueError, Collection.DoesNotExist):
            pass

    paginator = Paginator(videos, per_page=25)
    page = paginator.get_page(request.GET.get('p'))

    # Create response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        response = render(request, 'wagtailvideos/videos/results.html', {
            'videos': page,
            'query_string': query_string,
            'is_searching': bool(query_string),
        })
        return response
    else:
        response = render(request, 'wagtailvideos/videos/index.html', {
            'videos': page,
            'query_string': query_string,
            'is_searching': bool(query_string),
            'search_form': form,
            'popular_tags': popular_tags_for_model(Video),
            'current_collection': current_collection,
            'collections': collections_to_choose,
        })
        return response


@permission_checker.require('change')
def edit(request, video_id):
    Video = get_video_model()
    VideoForm = get_video_form(Video)
    video = get_object_or_404(Video, id=video_id)

    if request.POST:
        original_file = video.file
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            if 'file' in form.changed_data:
                # if providing a new video file, delete the old one and all renditions.
                # NB Doing this via original_file.delete() clears the file field,
                # which definitely isn't what we want...
                original_file.storage.delete(original_file.name)

                # Set new video file size
                video.file_size = video.file.size

            video = form.save()
            video.save()

            # Reindex the video to make sure all tags are indexed
            for backend in get_search_backends():
                backend.add(video)

            messages.success(request, _("Video '{0}' updated.").format(video.title))
        else:
            messages.error(request, _("The video could not be saved due to errors."))
    else:
        form = VideoForm(instance=video)

    if not video._meta.get_field('file').storage.exists(video.file.name):
        # Give error if video file doesn't exist
        messages.error(request, _(
            "The source video file could not be found. Please change the source or delete the video."
        ).format(video.title), buttons=[
            messages.button(reverse('wagtailvideos:delete', args=(video.id,)), _('Delete'))
        ])
    if is_modeladmin_installed():
        url_helper = AdminURLHelper(Video.get_track_listing_model())
        if hasattr(video, 'track_listing'):
            action_url = url_helper.get_action_url('edit', instance_pk=video.track_listing.pk)
        else:
            action_url = url_helper.create_url
    else:
        action_url = ''

    return render(request, "wagtailvideos/videos/edit.html", {
        'video': video,
        'form': form,
        'filesize': video.get_file_size(),
        'can_transcode': ffmpeg.installed() and not getattr(settings, 'WAGTAIL_VIDEOS_DISABLE_TRANSCODE', False),
        'transcodes': video.transcodes.all(),
        'transcode_form': VideoTranscodeAdminForm(video=video),
        'tracks_action_url': action_url,
        'user_can_delete': permission_policy.user_has_permission_for_instance(request.user, 'delete', video)
    })


@require_POST
def create_transcode(request, video_id):
    video = get_object_or_404(get_video_model(), id=video_id)
    transcode_form = VideoTranscodeAdminForm(data=request.POST, video=video)

    if transcode_form.is_valid():
        transcode_form.save()
    return redirect('wagtailvideos:edit', video_id)


@permission_checker.require('delete')
def delete(request, video_id):
    video = get_object_or_404(get_video_model(), id=video_id)

    if request.POST:
        video.delete()
        messages.success(request, _("Video '{0}' deleted.").format(video.title))
        return redirect('wagtailvideos:index')

    return render(request, "wagtailvideos/videos/confirm_delete.html", {
        'video': video,
    })


@permission_checker.require('add')
def add(request):
    Video = get_video_model()
    VideoForm = get_video_form(Video)

    if request.POST:
        video = Video(uploaded_by_user=request.user)
        form = VideoForm(request.POST, request.FILES, instance=video, user=request.user)
        if form.is_valid():
            # Save
            video = form.save(commit=False)
            video.file_size = video.file.size
            video.save()

            # Success! Send back an edit form
            for backend in get_search_backends():
                backend.add(video)

            messages.success(request, _("Video '{0}' added.").format(video.title), buttons=[
                messages.button(reverse('wagtailvideos:edit', args=(video.id,)), _('Edit'))
            ])
            return redirect('wagtailvideos:index')
        else:
            messages.error(request, _("The video could not be created due to errors."))
    else:
        form = VideoForm(user=request.user)

    return render(request, "wagtailvideos/videos/add.html", {
        'form': form,
    })


def usage(request, video_id):
    video = get_object_or_404(get_video_model(), id=video_id)

    paginator = Paginator(video.get_usage(), per_page=12)
    page = paginator.get_page(request.GET.get('p'))

    return render(request, "wagtailvideos/videos/usage.html", {
        'video': video,
        'used_by': page
    })
