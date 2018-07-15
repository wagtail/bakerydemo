import graphene
from graphene_django.types import DjangoObjectType
from . import models


class Location(DjangoObjectType):
    class Meta:
        model = models.LocationPage


class LocationOperatingHours(DjangoObjectType):
    class Meta:
        model = models.LocationOperatingHours


class Query(graphene.ObjectType):

    locations = graphene.List(Location)
    def resolve_locations(self, info):
        return models.LocationPage.objects.all()

    location = graphene.Field(Location, id=graphene.Int())
    def resolve_location(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return models.LocationPage.objects.get(pk=id)
