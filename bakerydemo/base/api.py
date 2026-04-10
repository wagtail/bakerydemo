from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView

from bakerydemo.base.models import Person


class PersonImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    url = serializers.SerializerMethodField()

    def get_url(self, image):
        request = self.context.get("request")
        url = image.file.url
        return request.build_absolute_uri(url) if request else url


class PersonSerializer(serializers.ModelSerializer):
    image = PersonImageSerializer(read_only=True)

    class Meta:
        model = Person
        fields = ("id", "first_name", "last_name", "job_title", "image")


class PersonQuerysetMixin:
    serializer_class = PersonSerializer

    def get_queryset(self):
        return Person.objects.filter(live=True).select_related("image").order_by(
            "last_name", "first_name"
        )


class PersonListAPIView(PersonQuerysetMixin, ListAPIView):
    pass


class PersonDetailAPIView(PersonQuerysetMixin, RetrieveAPIView):
    pass
