from wagtail.api.v2.views import BaseAPIViewSet

from .models import Person


class PersonApiViewSet(BaseAPIViewSet):
    model = Person
    name = "persons"
