import os
from embedding_base import EmbeddingProvider
from embedding_open_ai import OpenAIProvider

def get_embedding_provider() -> EmbeddingProvider:
    engine = os.getenv("EMBEDDING_ENGINE", "openai").lower()

    if engine == "openai":
        return OpenAIProvider()
    else:
        raise ValueError(f"Unsupported engine for: {engine}")