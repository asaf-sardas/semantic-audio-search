import yt_dlp
from fastapi import HTTPException

from models.content import SourceType
from schemas.content_schema import ContentPreviewResponse
from schemas.youtube.video_metadata import YoutubeVideoMetadata
from services.content_service.fetchers.base_content_fetcher import BaseContentFetcher


class YoutubeFetcher(BaseContentFetcher):
    def get_preview_content(self, url: str) -> ContentPreviewResponse:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'no_warnings': True,
            'extract_flat': False
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_metadata: YoutubeVideoMetadata = YoutubeVideoMetadata.model_validate(
                    ydl.extract_info(url, download=False))

                return ContentPreviewResponse(source_type=SourceType.YOUTUBE, **video_metadata.model_dump(by_alias=False))
        except yt_dlp.utils.DownloadError as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch video data. Check URL validity. Error: {str(e)}")
