from datetime import datetime, timezone
from pydantic import BaseModel, Field

class TrackSummary(BaseModel):
    album: str
    album_id: str
    artist: str
    artist_id: str
    duration: float
    title: str
    track_id: str

class TrackDetail(BaseModel):
    album: str
    album_id: str
    albumartist: str
    albumartist_id: str
    artist: str
    artist_id: str
    barcode: str
    bitdepth: int
    bitrate: float
    channels: int
    compilation: bool
    comment: str
    composer: str
    content_type: str
    copyright: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    date: str
    director: str
    directory: str
    duration: float
    disc_number: int
    disc_total: int
    filepath: str
    filesize: int
    genre: str
    isrc: str
    label: str
    lyrics: str
    samplerate: int
    title: str
    track_id: str
    track_number: int
    track_total: int
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    year: int

class TrackListResponse(BaseModel):
    items: list[TrackSummary]
    total: int