from django.utils.translation import ugettext_lazy as _

from generic_chooser.views import ModelChooserViewSet

from bakerydemo.base.models import People


class PersonChooserViewSet(ModelChooserViewSet):
    model = People