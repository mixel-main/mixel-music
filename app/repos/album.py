from typing import Any
from uuid import UUID

from sqlalchemy import delete, func, join, select, update
from sqlalchemy.dialects.sqlite import Insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncConnection

from app.models import Album, Artist


class AlbumRepo:
    def __init__(self, conn: AsyncConnection) -> None:
        self.conn = conn

    async def list_albums(self, offset: int, limit: int) -> tuple[list[dict[str, Any]], int]:
        album_query = await self.conn.execute(
            select(
                Album.album,
                Album.album_id,
                Artist.artist.label('albumartist'),
                Album.albumartist_id,
                Album.year,
            )
            .select_from(
                join(
                    Album, Artist,
                    Album.albumartist_id == Artist.artist_id
                )
            )
            .order_by(Album.album.asc())
            .offset(offset)
            .limit(limit)
        )
        album_list = [dict(row) for row in album_query.mappings().all()]

        total_query = await self.conn.execute(
            select(func.count()).select_from(Album)
        )
        total = total_query.scalar_one()
        return album_list, total
    
    async def get_album(self, album_id: UUID) -> dict[str, list[dict[str, Any] | None] | Any]:
        album_item = {}
        album_query = await self.conn.execute(
            select(
                Album.__table__,
                Artist.artist.label('albumartist')
            )
            .select_from(
                join(
                    Album, Artist,
                    Album.albumartist_id == Artist.artist_id
                )
            )
            .where(Album.album_id == album_id)
        )
        
        album_item = album_query.mappings().first()
        if album_item:
            album_item = dict(album_item)
        else:
            raise NoResultFound

        track_query = await self.conn.execute(
            select(
                Album.artist,
                Album.artist_id,
                Album.comment,
                Album.duration,
                Album.title,
                Album.track_id,
                Album.tracknumber,
            )
            .where(Album.album_id == album_id)
            .order_by(Album.track_number.asc())
        )
        album_item['tracks'] = [dict(row) for row in track_query.mappings().all()]
        return album_item

    async def insert_album(self, album_data: dict[str, Any]) -> None:
        await self.conn.execute(
            Insert(Album).values(**album_data).on_conflict_do_nothing()
        )
        
    async def update_album(self, album_id: UUID, album_data: dict[str, Any]) -> None:
        await self.conn.execute(
            update(Album)
            .values(**album_data)
            .where(Album.album_id == album_id)
        )

    async def delete_album(self, album_id: UUID) -> None:
        await self.conn.execute(
            delete(Album).where(Album.album_id == album_id)
        )
