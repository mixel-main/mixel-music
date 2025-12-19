import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.core.database import db_conn
from app.core.logger import get_logger
from app.repos.library import LibraryRepo
from app.utils.tags import extract_tags

logger = get_logger()

class LibraryTask:
    semaphore = asyncio.Semaphore(4)

    def __init__(self, path: str) -> None:
        self.path = path
        self.tags = {}

    async def create_track(self) -> None:
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as executor:
            self.tags = await loop.run_in_executor(executor, extract_tags, self.path)

        if self.tags:
            async with self.semaphore:
                async with db_conn() as conn:
                    repo = LibraryRepo(conn)
                    await repo.insert_track(self.tags)
                    logger.debug(f"Track inserted: {self.tags.get('title')}")

    async def remove_track(self) -> None:
        async with self.semaphore:
            async with db_conn() as conn:
                repo = LibraryRepo(conn)
                await repo.delete_track(self.path)
                logger.debug(f"Track removed: {self.path}")

    async def update_track(self) -> None:
        async with self.semaphore:
            async with db_conn() as conn:
                repo = LibraryRepo(conn)
                await repo.delete_track(self.path)
                await self.create_track()

                logger.debug(f"Track recreated: {self.path}")
