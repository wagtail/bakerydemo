from django.contrib.admin.utils import quote
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from generic_chooser.views import ModelChooserViewSet, ModelChooserMixin

from bakerydemo.base.models import People


class PersonChooserMixin(ModelChooserMixin):
    def get_edit_item_url(self, item):
        return reverse('wagtailsnippets:edit', args=('base', 'people', quote(item.pk)))

class PersonChooserViewSet(ModelChooserViewSet):
    icon = 'user'
    model = People
    page_title = _("Choose a person")
    per_page = 10
    order_by = 'last_name'
    fields = ['first_name', 'last_name', 'job_title']

    chooser_mixin_class = PersonChooserMixin