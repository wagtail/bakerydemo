import graphene
from graphene_django.types import DjangoObjectType
from bakerydemo.base.models import People

from . import models
import bakerydemo.helpers


class Author(DjangoObjectType):
    class Meta:
        model = People

class Blog(DjangoObjectType):
    class Meta:
        model = models.BlogPage

    authors = graphene.List(Author)
    def resolve_authors(self, info):
        return self.authors()



class Query(graphene.ObjectType):

    blogs = graphene.List(Blog, id=graphene.Int())
    def resolve_blogs(self, info):
        return models.BlogPage.objects.all()

    blog = graphene.Field(Blog)
    def resolve_blog(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return models.BlogPage.objects.get(pk=id)