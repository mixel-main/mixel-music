import aiofiles
import aiofiles.os
import asyncio
from datetime import datetime, timezone
from uuid import UUID

from app.repos import LibraryRepos
from app.services import BaseService
from app.infra.path import get_path
from app.infra.tags import extract_tags


class LibraryService(BaseService):
    semaphore = asyncio.Semaphore(4)

    def __init__(self, repo: LibraryRepos) -> None:
        self.repo = repo

    async def list_albums(self, offset: int, limit: int):
        return await self.repo.album.list_albums(offset, limit)
    
    async def get_album(self, album_id: UUID):
        return await self.repo.album.get_album(album_id)

    async def list_artists(self, offset: int, limit: int):
        return await self.repo.artist.list_artists(offset, limit)
    
    async def get_artist(self, artist_id: UUID):
        return await self.repo.artist.get_artist(artist_id)

    async def list_tracks(self, offset: int, limit: int):
        return await self.repo.track.list_tracks(offset, limit)

    async def get_track(self, track_id: UUID):
        return await self.repo.track.get_track(track_id)
    
    async def create_track(self, path) -> None:
        tags = await extract_tags(path)

        if tags:
            post_value = {
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
                "missing": False,
            }

            tags = tags | post_value

            async with self.semaphore:
                await self.repo.track.insert_track(tags)
                self.logger.debug(f"Track inserted: {tags.get('title')}")

    async def fs_events(self, events):
        from app.infra.watcher import FsEventType

        tasks = []

        for e in events:
            if e.type == FsEventType.DEL:
                tasks.append(self.repo.track.delete_track_path(e.path))

            elif e.type in (FsEventType.ADD, FsEventType.MOD):
                real_path = get_path(e.path)
                if await aiofiles.os.path.exists(real_path):
                    tasks.append(self.create_track(e.path))
                else:
                    tasks.append(self.repo.track.delete_track_path(e.path))

        if tasks:
            await asyncio.gather(*tasks)

    async def streaming(self, track_id: str, range_header: str | None):
        path = await self.repo.track.get_filepath_by_track_id(track_id)
        track = await self.repo.track.get_track(track_id)

        real_path = get_path(path)
        track_size = track["filesize"]
        mime_type = track["content_type"]

        chunk_size = int(track_size * 0.25)

        if range_header:
            try:
                start_str, end_str = range_header.replace("bytes=", "").split("-")
                start = int(start_str)
                end = int(end_str) if end_str else start + chunk_size
            except ValueError:
                start, end = 0, 0
        else:
            start = 0
            end = start + chunk_size

        end = min(end, track_size - 1)

        if start == 0:
            self.logger.debug(
                'Streaming "%s" (%s-%s)',
                track["title"],
                start,
                end,
            )

        async with aiofiles.open(real_path, "rb") as f:
            await f.seek(start)
            data = await f.read(end - start + 1)

        headers = {
            "Content-Range": f"bytes {start}-{end}/{track_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(end - start + 1),
            "Content-Type": mime_type,
        }

        return data, headers
