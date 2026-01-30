import logging

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install

from app.core.config import get_config

_console = Console(record=False, soft_wrap=True)


def setup_logging() -> None:
    root = logging.getLogger()
    if getattr(root, "_is_ready", False):
        return

    config = get_config()

    install(word_wrap=True)

    rich_handler = RichHandler(console=_console, rich_tracebacks=True)
    root.setLevel(config.LOG_LEVEL)
    root.addHandler(rich_handler)

    if config.LOG_PATH is not None:
        file_handler = logging.FileHandler(config.LOG_PATH, mode="a", encoding="utf-8")
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        root.addHandler(file_handler)

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.propagate = True
        logger.setLevel(logging.INFO)

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)
    logging.getLogger("watchfiles").setLevel(logging.WARNING)

    root._is_ready = True


def get_logger(name: str = __name__) -> logging.Logger:
    return logging.getLogger(name)
