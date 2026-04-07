from abc import ABC, abstractmethod

class AudioExtractor(ABC):
    @abstractmethod
    def download_and_extract(self, url: str, output_path: str) -> str:
        pass