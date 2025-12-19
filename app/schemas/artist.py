from pydantic import BaseModel

class ArtistAlbum(BaseModel):
    album: str
    album_id: str
    year: int

class ArtistSummary(BaseModel):
    artist: str
    artist_id: str

class ArtistDetail(BaseModel):
    artist: str
    artist_id: str
    albums: list[ArtistAlbum]

class ArtistListResponse(BaseModel):
    items: list[ArtistSummary]
    total: int
