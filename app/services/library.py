import aiofiles
from app.core.logger import get_logger
from app.repos.library import LibraryRepo
from app.utils.path import get_path

logger = get_logger()

class LibraryService:
    def __init__(self, repo: LibraryRepo) -> None:
        self.repo = repo

    # Track

    async def list_tracks(self, offset: int, limit: int):
        return await self.repo.list_tracks(offset, limit)

    async def get_track(self, id: str):
        return await self.repo.get_track(id)

    # Album

    async def list_albums(self, offset: int, limit: int):
        return await self.repo.list_albums(offset, limit)

    async def get_album(self, album_id: str):
        return await self.repo.get_album(album_id)

    # Artist

    async def list_artists(self, offset: int, limit: int):
        return await self.repo.list_artists(offset, limit)

    async def get_artist(self, artist_id: str):
        return await self.repo.get_artist(artist_id)

    # Streaming

    async def stream_track(self, track_id: str, range_header: str | None):
        path = await self.repo.get_path_by_track_id(track_id)
        track = await self.repo.get_track(track_id)

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
            logger.debug(
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
