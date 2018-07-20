from __future__ import unicode_literals

import graphene
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from wagtail.core.models import get_page_models, Page
from graphene_django.types import DjangoObjectType

from bakerydemo.breads.schema import Query as BreadQuery
from bakerydemo.locations.schema import Query as LocationQuery
from bakerydemo.blog.schema import Query as BlogQuery, Blog


class ContentTypeDjangoObjectType(DjangoObjectType):
    class Meta:
        model = ContentType


def generate_graphene_objects_for_all_page_types():
    models = get_page_models()
    graphene_objects = []
    for model in models:
        graphene_object = type(
            f'{model.__name__}',
            (DjangoObjectType,),
            {'Meta': type('Meta', (object,), {'model': model})}
        )
        graphene_objects.append(graphene_object)
    return graphene_objects


class SpecificPage(graphene.Union):
    class Meta:
        types = generate_graphene_objects_for_all_page_types()


class PageDjangoObjectType(DjangoObjectType):
    specific = graphene.List(SpecificPage)
    content_type = graphene.Field(ContentTypeDjangoObjectType)

    def resolve_specific(self, info, **kwargs):
        return [self.specific]

    class Meta:
        model = Page
        filter_fields = ['title']


class PagesRootQuery(graphene.ObjectType):
    all = graphene.List(PageDjangoObjectType, content_types=graphene.String())

    def resolve_all(self, info, **kwargs):
        qs = Page.objects.live().public()
        content_types = kwargs.get('content_types')
        if content_types is not None:
            content_types = [content_type.split('.') for content_type
                             in content_types.split(',')]
            content_type_q = Q()
            for content_type in content_types:
                content_type_q |= Q(app_label=content_type[0],
                                    model=content_type[1])
            content_types = (
                ContentType.objects.filter(content_type_q)
                                   .values_list('pk', flat=True)
            )
            qs = qs.filter(content_type_id__in=content_types)
        return qs



class Query(PagesRootQuery, BlogQuery, LocationQuery, BreadQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
