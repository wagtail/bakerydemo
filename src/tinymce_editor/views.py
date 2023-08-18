from wagtailvideos import get_video_model
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def get_video_url(request, video_id=None):
    video = get_object_or_404(get_video_model(), id=video_id)
    return JsonResponse({'media_url': video.url})
