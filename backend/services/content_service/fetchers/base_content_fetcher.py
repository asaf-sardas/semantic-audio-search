from abc import ABC, abstractmethod

from schemas.content_schema import ContentPreviewResponse


class BaseContentFetcher(ABC):
    @abstractmethod
    def get_preview_content(self, url: str) -> ContentPreviewResponse:
        pass