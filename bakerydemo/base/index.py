from django.utils.functional import classproperty
from django_ai_core.contrib.index import (
    CachedEmbeddingTransformer,
    CoreEmbeddingTransformer,
    VectorIndex,
    registry,
)
from django_ai_core.contrib.index.source import ModelSource
from django_ai_core.contrib.index.storage.pgvector import PgVectorProvider
from wagtail_ai.agents.base import get_llm_service

from bakerydemo.blog.models import BlogPage


@registry.register()
class PageIndex(VectorIndex):
    sources = [
        ModelSource(
            model=BlogPage,
        ),
    ]
    storage_provider = PgVectorProvider()

    # Use classproperty to avoid creating LLMService instance at import time,
    # as it requires API keys to be set in environment, which is not necessary
    # during collectstatic etc at build time.
    @classproperty
    def embedding_transformer(cls):
        llm_service = get_llm_service("embedding")
        return CachedEmbeddingTransformer(
            base_transformer=CoreEmbeddingTransformer(llm_service=llm_service),
        )
