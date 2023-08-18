from django.conf import settings
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import View
from wagtail.admin.auth import PermissionPolicyChecker
from wagtail.admin.models import popular_tags_for_model
from wagtail.admin.views.generic.chooser import (
    BaseChooseView, ChooseResultsViewMixin, ChooseViewMixin,
    ChosenResponseMixin, ChosenViewMixin, CreateViewMixin, CreationFormMixin)
from wagtail.admin.viewsets.chooser import ChooserViewSet

from src.wagtailvideos import get_video_model
from src.wagtailvideos.forms import get_video_form
from src.wagtailvideos.permissions import permission_policy

permission_checker = PermissionPolicyChecker(permission_policy)


class VideoChosenResponseMixin(ChosenResponseMixin):
    def get_chosen_response_data(self, video):
        response_data = super().get_chosen_response_data(video)
        response_data["preview"] = {
            "url": video.thumbnail.url if video.thumbnail else "",
            "width": 165,
            "height": 165,
        }
        return response_data


class VideoCreationFormMixin(CreationFormMixin):
    creation_tab_id = "upload"
    create_action_label = _("Upload")
    create_action_clicked_label = _("Uploading…")
    permission_policy = permission_policy

    def get_creation_form_class(self):
        return get_video_form(self.model)

    def get_creation_form_kwargs(self):
        kwargs = super().get_creation_form_kwargs()
        if self.request.method in ("POST", "PUT"):
            kwargs["instance"] = self.model(uploaded_by_user=self.request.user)
        return kwargs


class BaseVideoChooseView(BaseChooseView):
    template_name = "wagtailvideos/chooser/chooser.html"
    results_template_name = "wagtailvideos/chooser/results.html"
    per_page = getattr(settings, "WAGTAILVIDEOS_CHOOSER_PAGE_SIZE", 12)
    ordering = "-created_at"

    def get_object_list(self):
        return (
            permission_policy.instances_user_has_any_permission_for(
                self.request.user, ["choose"]
            )
            .select_related("collection")
        )

    def filter_object_list(self, objects):
        tag_name = self.request.GET.get("tag")
        if tag_name:
            objects = objects.filter(tags__name=tag_name)
        return super().filter_object_list(objects)

    def get_filter_form(self):
        FilterForm = self.get_filter_form_class()
        return FilterForm(self.request.GET, collections=self.collections)

    @cached_property
    def collections(self):
        collections = self.permission_policy.collections_user_has_permission_for(
            self.request.user, "choose"
        )
        if len(collections) < 2:
            return None

        return collections

    def get(self, request):
        self.model = get_video_model()
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "collections": self.collections,
            }
        )
        return context


class VideoChooseViewMixin(ChooseViewMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_tags"] = popular_tags_for_model(self.model)
        return context

    def get_response_json_data(self):
        json_data = super().get_response_json_data()
        json_data["tag_autocomplete_url"] = reverse("wagtailadmin_tag_autocomplete")
        return json_data


class VideoChooseView(
    VideoChooseViewMixin, VideoCreationFormMixin, BaseVideoChooseView
):
    pass


class VideoChooseResultsView(
    ChooseResultsViewMixin, VideoCreationFormMixin, BaseVideoChooseView
):
    pass


class VideoChosenView(ChosenViewMixin, VideoChosenResponseMixin, View):
    def get(self, request, *args, pk, **kwargs):
        self.model = get_video_model()
        return super().get(request, *args, pk, **kwargs)


class VideoUploadViewMixin(CreateViewMixin):
    def get(self, request):
        self.model = get_video_model()
        return super().get(request)

    def post(self, request):
        self.model = get_video_model()
        self.form = self.get_creation_form()

        if self.form.is_valid():
            image = self.save_form(self.form)

            # not specifying a format; return the image details now
            return self.get_chosen_response(image)

        else:  # form is invalid
            return self.get_reshow_creation_form_response()


class VideoUploadView(
    VideoUploadViewMixin, VideoCreationFormMixin, VideoChosenResponseMixin, View
):
    pass


class VideoChooserViewSet(ChooserViewSet):
    choose_view_class = VideoChooseView
    choose_results_view_class = VideoChooseResultsView
    chosen_view_class = VideoChosenView
    create_view_class = VideoUploadView
    permission_policy = permission_policy
    register_widget = False

    icon = "media"
    choose_one_text = _("Choose a video")
    create_action_label = _("Upload")
    create_action_clicked_label = _("Uploading…")


viewset = VideoChooserViewSet(
    "wagtailvideos_chooser",
    model=get_video_model(),
    url_prefix="videos/chooser",
)
