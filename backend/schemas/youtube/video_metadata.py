from pydantic import BaseModel, Field

class YoutubeVideoMetadata(BaseModel):
    id: str
    title: str
    thumbnail_url: str = Field(alias="thumbnail")
    duration: int
    url: str