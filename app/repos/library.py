from typing import Any
from app.core.database import (
    AsyncConnection,
    select,
    insert,
    Insert,
    delete,
    NoResultFound,
    or_,
    join,
    func,
)
from app.models import Album, Artist, Track

class LibraryRepo:
    def __init__(self, conn: AsyncConnection) -> None:
        self.conn = conn

    # Track

    async def list_tracks(self, offset: int, limit: int) -> tuple[list[dict[str, Any]], int]:
        db_query = await self.conn.execute(
            select(
                Track.album,
                Track.album_id,
                Track.artist,
                Track.artist_id,
                Track.duration,
                Track.title,
                Track.track_id,
            )
            .order_by(Track.title.asc())
            .offset(offset)
            .limit(limit)
        )
        track_list = [dict(row) for row in db_query.mappings().all()]

        total_query = await self.conn.execute(
            select(func.count()).select_from(Track)
        )
        total = total_query.scalar_one()
        return track_list, total
    
    async def get_track(self, track_id: str) -> dict[str, Any]:
        track_item = {}
        db_query = await self.conn.execute(
            select(Track.__table__).where(Track.track_id == track_id)
        )
        track_item = db_query.mappings().first()

        if track_item:
            return dict(track_item)
        else:
            raise NoResultFound
        
    async def insert_track(self, track_data: dict[str, Any]) -> None:
        await self.conn.execute(
            insert(Track).values(**track_data)
        )

    async def delete_track(self, filepath: str) -> None:
        await self.conn.execute(
            delete(Track).where(Track.filepath == filepath)
        )

    # Album

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
    
    async def get_album(self, album_id: str) -> dict[str, list[dict[str, Any] | None] | Any]:
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
                Track.artist,
                Track.artist_id,
                Track.comment,
                Track.duration,
                Track.title,
                Track.track_id,
                Track.track_number,
            )
            .where(Track.album_id == album_id)
            .order_by(Track.track_number.asc())
        )
        album_item['tracks'] = [dict(row) for row in track_query.mappings().all()]
        return album_item

    async def insert_album(self, album_data: dict[str, Any]) -> None:
        await self.conn.execute(
            Insert(Album).values(**album_data).on_conflict_do_nothing()
        )

    async def delete_album(self, album_id: str) -> None:
        await self.conn.execute(
            delete(Album).where(Album.album_id == album_id)
        )

    # Artist

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

    async def get_artist(self, artist_id: str) -> dict[str, list[dict[str, Any]] | Any]:
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

    async def delete_artist(self, artist_id: str) -> None:
        await self.conn.execute(
            delete(Artist).where(Artist.artist_id == artist_id)
        )
    
    # Library

    async def get_scan_info(self) -> Any:
        result = await self.conn.execute(select(Track.filepath, Track.filesize))
        result = result.all()

        return result
    
    async def get_item_path(self, item_id: str) -> dict[Any, Any]:
        result = await self.conn.execute(
            select(Track.filepath)
            .where(
                or_(Track.album_id == item_id, Track.track_id == item_id)
            )
        )

        data = result.mappings().first()
        return dict(data) if data else {}
    
    async def get_path_by_track_id(self, track_id: str) -> str:
        result = await self.conn.execute(
            select(Track.filepath).where(Track.track_id == track_id)
        )

        row = result.scalars().first()
        return row if row else ''
