import graphene
from graphene_django.types import DjangoObjectType
from . import models
import bakerydemo.graphql.helpers


class Bread(DjangoObjectType):
    class Meta:
        model = models.BreadPage


class BreadType(DjangoObjectType):
    class Meta:
        model = models.BreadType


class Ingredient(DjangoObjectType):
    class Meta:
        model = models.BreadIngredient


class Country(DjangoObjectType):
    class Meta:
        model = models.Country


class Query(graphene.ObjectType):

    breads = graphene.List(Bread)
    def resolve_breads(self, info):
        return models.BreadPage.objects.all()

    bread = graphene.Field(Bread, id=graphene.Int())
    def resolve_bread(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return models.BreadPage.objects.get(pk=id)
