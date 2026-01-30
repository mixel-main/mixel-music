import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from app.core.config import ensure_dirs, get_config
from app.core.database import connect_db, disconnect_db
from app.core.logger import get_logger, setup_logging
from app.infra.watcher import watcher, FsEvent
from app.services.fs_event import fs_event

setup_logging()

config = get_config()
logger = get_logger()


async def _bg(name: str, coro) -> None:
    try:
        await coro
    except asyncio.CancelledError:
        logger.info("Task '%s' cancelled", name)
        raise
    except Exception:
        logger.exception("Task '%s' crashed", name)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    ensure_dirs()

    await connect_db()

    app.state.event_queue = asyncio.Queue(maxsize=200)

    app.state.background_tasks = [
        asyncio.create_task(_bg("watcher", watcher(app.state.event_queue))),
        asyncio.create_task(_bg("fs_event", fs_event(app.state.event_queue))),
    ]

    try:
        yield
    finally:
        for t in app.state.background_tasks:
            t.cancel()

        await asyncio.gather(*app.state.background_tasks, return_exceptions=True)

        await disconnect_db()


app = FastAPI(
    debug=config.DEBUG,
    title="mixel-music",
    version=config.VERSION,
    lifespan=lifespan,
    docs_url=None
)


if config.DEBUG:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_docs() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"API • {app.title}",
            swagger_css_url="https://cdn.jsdelivr.net/gh/mixel-music/swagger-ui-dark/dark.css",
        )


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=config.HOST,
        port=config.PORT,
        reload=True,
        log_level=config.LOG_LEVEL,
        log_config=None,
    )
