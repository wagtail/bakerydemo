from django_ai_core.contrib.index import (
    CachedEmbeddingTransformer,
    CoreEmbeddingTransformer,
    VectorIndex,
    registry,
)
from django_ai_core.contrib.index.source import ModelSource
from django_ai_core.contrib.index.storage.pgvector import PgVectorProvider
from django_ai_core.llm import LLMService

from bakerydemo.blog.models import BlogPage

llm_embedding_service = LLMService.create(
    provider="openai", model="text-embedding-3-small"
)


@registry.register()
class PageIndex(VectorIndex):
    sources = [
        ModelSource(
            model=BlogPage,
        ),
    ]
    storage_provider = PgVectorProvider()
    embedding_transformer = CachedEmbeddingTransformer(
        base_transformer=CoreEmbeddingTransformer(llm_service=llm_embedding_service),
    )
