from typing import Any
from uuid import UUID

from sqlalchemy import delete, func, or_, select, update
from sqlalchemy.dialects.sqlite import Insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncConnection

from app.models import Album, Artist, Track


class ArtistRepo:
    def __init__(self, conn: AsyncConnection) -> None:
        self.conn = conn

    async def list_artists(self, offset: int, limit: int) -> tuple[list[dict[str, Any]], int]:
        db_query = await self.conn.execute(
            select(Artist.__table__)
            .order_by(Artist.artist.asc())
            .offset(offset)
            .limit(limit)
        )
        artist_list = [dict(row) for row in db_query.mappings().all()]

        total_query = await self.conn.execute(
            select(func.count()).select_from(Artist)
        )
        total = total_query.scalar_one()
        return artist_list, total

    async def get_artist(self, artist_id: UUID) -> dict[str, list[dict[str, Any]] | Any]:
        artist_item = {}
        track_query = await self.conn.execute(
            select(Track.album_id)
            .where(or_(Track.artist_id == artist_id, Track.albumartist_id == artist_id))
        )
        tracks_data = track_query.mappings().all()

        if tracks_data:
            # Search album using album_id if tracks_data available
            album_ids = [track['album_id'] for track in tracks_data]
            album_from_tracks_query = await self.conn.execute(
                select(
                    Album.album,
                    Album.album_id,
                    Album.albumartist_id,
                    Album.year,
                )
                .where(Album.album_id.in_(album_ids))
                .order_by(Album.year.asc())
            )
            
            albums_data = album_from_tracks_query.mappings().all()
            albums_data = [dict(album) for album in albums_data]

            if albums_data:
                album = albums_data[0]
                
                # Lookup artist using albumartist_id
                artist_query = await self.conn.execute(
                    select(Artist.__table__)
                    .where(Artist.artist_id == album['albumartist_id'])
                )
                artist_data = artist_query.mappings().first()

                if artist_data:
                    artist_item = {
                        'artist': artist_data['artist'],
                        'artist_id': artist_id,
                        'albums': albums_data
                    }
        else:
            raise NoResultFound

        return artist_item
    
    async def insert_artist(self, artist_data: dict[str, Any]) -> None:
        await self.conn.execute(
            Insert(Artist)
            .values(**artist_data)
            .on_conflict_do_update(
                index_elements=['artist_id'],
                set_=artist_data
            )
        )

    async def update_artist(self, artist_id: UUID, artist_data: dict[str, Any]) -> None:
        await self.conn.execute(
            update(Artist)
            .values(**artist_data)
            .where(Artist.artist_id == artist_id)
        )

    async def delete_artist(self, artist_id: UUID) -> None:
        await self.conn.execute(
            delete(Artist).where(Artist.artist_id == artist_id)
        )
