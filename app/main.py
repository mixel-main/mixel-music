import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any
from diskcache import Cache
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from app.api import api_router
from app.core.config import get_config
from app.core.database import connect_database, disconnect_database
from app.core.logger import get_logger, setup_logging
from app.core.middleware import CustomSessionMiddleware
from app.services.auth import AuthService
from app.services.scanner import scanner, tracker

setup_logging()
logger = get_logger()
config = get_config()

async def _bg(name: str, coro):
    try:
        await coro
    except asyncio.CancelledError:
        logger.info("Task '%s' cancelled", name)
        raise
    except Exception:
        logger.exception("Task '%s' crashed", name)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    config.ARTWORK_DIR.mkdir(parents=True, exist_ok=True)

    app.state.session_cache = Cache(config.DATA_DIR)
    app.state.auth_service = AuthService(app.state.session_cache)

    await connect_database()

    app.state.background_tasks = [
        asyncio.create_task(_bg("scanner", scanner())),
        asyncio.create_task(_bg("tracker", tracker())),
    ]

    try:
        yield
    finally:
        for t in app.state.background_tasks:
            t.cancel()
        await asyncio.gather(*app.state.background_tasks, return_exceptions=True)

        await disconnect_database()

app = FastAPI(
    debug=config.DEBUG,
    title=config.APP_NAME,
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

app.add_middleware(CustomSessionMiddleware)
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level=config.LOG_LEVEL.lower(),
        log_config=None,
    )
