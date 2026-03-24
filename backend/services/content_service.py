import yt_dlp
from typing import Callable
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.models.content import Content, ContentStatus, SourceType
from backend.schemas.content_schema import ContentCreate


def _fetch_youtube_metadata(url: str) -> dict:
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
        'extract_flat': False
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info:
                raise HTTPException(status_code=400, detail="Playlists are not supported. Please provide a single video URL.")
                
            return {
                "id": info.get("id"),
                "title": info.get("title"),
                "thumbnail_url": info.get("thumbnail"),
                "duration": info.get("duration"),
            }
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch video data. Check URL validity. Error: {str(e)}")


def _fetch_podcast_metadata(url: str) -> dict:
    raise HTTPException(status_code=501, detail="Podcast processing is not implemented yet.")


_METADATA_FETCHERS: dict[SourceType, Callable[[str], dict]] = {
    SourceType.YOUTUBE: _fetch_youtube_metadata,
    SourceType.PODCAST: _fetch_podcast_metadata,
}


def _get_fetcher(source_type: SourceType) -> Callable[[str], dict]:
    fetcher = _METADATA_FETCHERS.get(source_type)
    if not fetcher:
        raise HTTPException(status_code=400, detail=f"Source type {source_type} is not supported.")
    return fetcher


def preview_content(payload: ContentCreate) -> dict:
    fetcher = _get_fetcher(payload.source_type)
    metadata = fetcher(payload.url)
    
    return {
        "url": payload.url,
        "title": metadata["title"],
        "thumbnail_url": metadata["thumbnail_url"],
        "duration": metadata["duration"],
        "source_type": payload.source_type
    }


def process_content(db: Session, payload: ContentCreate) -> Content:
    fetcher = _get_fetcher(payload.source_type)

    existing_content = db.query(Content).filter(Content.url == payload.url).first()
    
    if existing_content:
        if existing_content.status == ContentStatus.FAILED:
            existing_content.status = ContentStatus.PENDING
            db.commit()
            db.refresh(existing_content)
            return existing_content
        return existing_content

    metadata = fetcher(payload.url)

    new_content = Content(
        id=metadata["id"], 
        title=metadata["title"],
        url=payload.url,
        thumbnail_url=metadata["thumbnail_url"],
        duration=metadata["duration"],
        source_type=payload.source_type,
        status=ContentStatus.PENDING
    )
    
    try:
        db.add(new_content)
        db.commit()
        db.refresh(new_content)
    except IntegrityError:
        db.rollback()
        existing_content = db.query(Content).filter(Content.url == payload.url).first()
        if existing_content:
            return existing_content
        raise HTTPException(status_code=500, detail="Database error occurred.")

    return new_content


def get_content_by_id(db: Session, content_id: str) -> Content:
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content