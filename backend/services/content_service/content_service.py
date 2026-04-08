from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.content import Content, ContentStatus, SourceType
from schemas.content_schema import ContentCreate, ContentPreviewResponse, ContentRead
from services.content_service.fetchers.base_content_fetcher import BaseContentFetcher
from services.content_service.fetchers.youtube_fetcher import YoutubeFetcher

def _fetch_podcast_metadata(url: str) -> dict:
    raise HTTPException(status_code=501, detail="Podcast processing is not implemented yet.")


_METADATA_FETCHERS: dict[SourceType, BaseContentFetcher] = {
    SourceType.YOUTUBE: YoutubeFetcher(),

}


def _get_fetcher(source_type: SourceType) -> BaseContentFetcher:
    fetcher: BaseContentFetcher = _METADATA_FETCHERS.get(source_type)
    if not fetcher:
        raise HTTPException(status_code=400, detail=f"Source type {source_type} is not supported.")

    return fetcher


def preview_content(payload: ContentCreate) -> ContentPreviewResponse:
    fetcher: BaseContentFetcher = _get_fetcher(source_type=payload.source_type)
    metadata: ContentPreviewResponse = fetcher.get_preview_content(url=payload.url)

    return metadata


def process_content(db: Session, payload: ContentCreate) -> Content:
    fetcher: BaseContentFetcher = _get_fetcher(source_type=payload.source_type)

    existing_content= db.query(Content).filter(Content.url == payload.url).first()
    
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
    content= db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content