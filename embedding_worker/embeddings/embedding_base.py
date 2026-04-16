from abc import ABC, abstractmethod

class EmbeddingProvider(ABC):

    @property
    @abstractmethod
    def dimension(self) -> int:
        pass

    @property
    @abstractmethod
    def collection_name(self) -> str:
        pass

    @abstractmethod
    def generate_embeddings(self,chunks:list)->list:
        pass