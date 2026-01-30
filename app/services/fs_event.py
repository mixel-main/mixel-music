import asyncio

from app.core.dependencies import get_library_service
from app.core.logger import get_logger
from app.infra.watcher import FsEvent


async def fs_event(event_queue: asyncio.Queue[list[FsEvent]]) -> None:
    logger = get_logger()

    while True:
        events = await event_queue.get()
        try:
            async with get_library_service() as service:
                await service.fs_events(events)
        except Exception:
            logger.exception("Failed to process fs events batch.")
        finally:
            event_queue.task_done()
