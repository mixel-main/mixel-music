from fastapi import Depends
from contextlib import asynccontextmanager

from app.core.database import AsyncGenerator, db_session
from app.repos import LibraryRepos, AlbumRepo, ArtistRepo, TrackRepo
from app.services.library import LibraryService


async def get_album_repo() -> AsyncGenerator[AlbumRepo, None]:
    async with db_session() as conn:
        yield AlbumRepo(conn)


async def get_artist_repo() -> AsyncGenerator[ArtistRepo, None]:
    async with db_session() as conn:
        yield ArtistRepo(conn)


async def get_track_repo() -> AsyncGenerator[TrackRepo, None]:
    async with db_session() as conn:
        yield TrackRepo(conn)


async def get_library_repo() -> AsyncGenerator[LibraryRepos, None]:
    async with db_session() as conn:
        yield LibraryRepos(conn)


@asynccontextmanager
async def get_library_service():
    async with db_session() as conn:
        repo = LibraryRepos(conn)
        service = LibraryService(repo)
        yield service
