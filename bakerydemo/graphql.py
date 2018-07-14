from __future__ import unicode_literals
import graphene
from graphene_django import DjangoObjectType
from bakerydemo.breads.models import BreadType


class Bread(DjangoObjectType):
    class Meta:
        model = BreadType


class Query(graphene.ObjectType):
    breads = graphene.List(Bread)

    def resolve_breads(self, info):
        return BreadType.objects.all()

schema = graphene.Schema(query=Query)