from sqlalchemy.ext.asyncio import AsyncConnection

from .album import AlbumRepo
from .artist import ArtistRepo
from .track import TrackRepo


class LibraryRepos:
    def __init__(self, conn: AsyncConnection) -> None:
        self.album = AlbumRepo(conn)
        self.artist = ArtistRepo(conn)
        self.track = TrackRepo(conn)
