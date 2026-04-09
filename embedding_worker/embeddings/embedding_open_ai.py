from embedding_base import EmbeddingProvider
import os
from openai import OpenAI

class OpenAIProvider(EmbeddingProvider):
    def __init__(self):
        self.client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "text-embedding-3-small"

    @property
    def dimension(self) -> int:
        return 1536

    @property
    def collection_name(self) -> str:
        return "openai"

    def generate_embeddings(self,chunks:list) ->list:
        if not chunks:
            return []
        texts = [chunk["text"] for chunk in chunks]
        response = self.client.embeddings.create(input=texts, model=self.model)
        for i, chunk in enumerate(chunks):
            chunk["embedding"] = response.data[i].embedding
        return chunks
