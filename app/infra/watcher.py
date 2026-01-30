import asyncio
from dataclasses import dataclass
from enum import Enum, auto

from watchfiles import Change, awatch

from app.core.config import get_config
from app.core.logger import get_logger
from app.infra.path import str_path, is_supported_file


class FsEventType(str, Enum):
    ADD = auto()
    MOD = auto()
    DEL = auto()


@dataclass(frozen=True)
class FsEvent:
    type: FsEventType
    path: str


_CHANGE_EVENT_TYPE = {
    Change.added: FsEventType.ADD,
    Change.modified: FsEventType.MOD,
    Change.deleted: FsEventType.DEL,
}


def _normalize_batch(batch) -> list[FsEvent]:
    last: dict[str, Change] = {}

    for change, raw_path in batch:
        path = str_path(raw_path)
        if not is_supported_file(path):
            continue

        last[path] = change

    events: list[FsEvent] = []
    for path, change in last.items():
        type = _CHANGE_EVENT_TYPE.get(change)

        if type:
            events.append(FsEvent(type=type, path=path))

    order = {FsEventType.DEL: 0, FsEventType.ADD: 1, FsEventType.MOD: 2}
    events.sort(key=lambda event: order[event.type])

    return events


async def watcher(event_queue: asyncio.Queue[list[FsEvent]]) -> None:
    logger = get_logger()
    config = get_config()

    logger.info("Started watching for library.")

    async for batch in awatch(
        config.LIBRARY_DIR,
        force_polling=True,
        recursive=True,
    ):
        events = _normalize_batch(batch)
        if not events:
            continue

        await event_queue.put(events)
