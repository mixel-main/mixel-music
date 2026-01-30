from pydantic import BaseModel

class AlbumTrack(BaseModel):
    artist: str
    artist_id: str
    comment: str
    duration: float
    title: str
    track_id: str
    track_number: int

class AlbumSummary(BaseModel):
    album: str
    album_id: str
    albumartist: str
    albumartist_id: str
    year: int

class AlbumDetail(BaseModel):
    album: str
    album_id: str
    albumartist: str
    albumartist_id: str
    disc_total: int
    year: int
    tracks: list[AlbumTrack]

class AlbumListResponse(BaseModel):
    items: list[AlbumSummary]
    total: int
