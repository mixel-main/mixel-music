from typing import Any
from uuid import UUID

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncConnection

from app.models import Track


class TrackRepo:
    def __init__(self, conn: AsyncConnection) -> None:
        self.conn = conn

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
    
    async def get_track(self, track_id: UUID) -> dict[str, Any]:
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

    async def update_track(self, track_id: UUID, track_data: dict[str, Any]) -> None:
        await self.conn.execute(
            update(Track)
            .values(**track_data)
            .where(Track.track_id == track_id)
        )

    async def update_track_path(self, track_path: str, track_data: dict[str, Any]) -> None:
        await self.conn.execute(
            update(Track)
            .values(**track_data)
            .where(Track.filepath == track_path)
        )

    async def delete_track(self, track_id: UUID) -> None:
        await self.conn.execute(
            delete(Track).where(Track.track_id == track_id)
        )

    async def delete_track_path(self, track_path: UUID) -> None:
        await self.conn.execute(
            delete(Track).where(Track.filepath == track_path)
        )

    async def get_filepath_filesize(self) -> Any:
        result = await self.conn.execute(select(Track.filepath, Track.filesize))
        result = result.all()

        return result

    async def get_filepath_by_track_id(self, track_id: UUID) -> str:
        result = await self.conn.execute(
            select(Track.filepath).where(Track.track_id == track_id)
        )

        row = result.scalars().first()
        return row if row else ''
