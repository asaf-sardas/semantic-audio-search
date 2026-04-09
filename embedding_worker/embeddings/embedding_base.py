from abc import ABC, abstractmethod

class EmbeddingProvider(ABC):
    @abstractmethod
    def generate_embeddings(self,chunks:list)->list:
        pass