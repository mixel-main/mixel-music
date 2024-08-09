from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import asyncio

from api import albums, artists, artwork, stream, tracks
from core.watcher import find_changes, watch_change
from infra.config import *
from infra.database import *
from infra.loggings import *

@asynccontextmanager
async def init(app: FastAPI):
    create_dir(conf)
    log = log_file_handler()
    await connect_database()
    
    asyncio.create_task(find_changes())
    asyncio.create_task(watch_change())

    try:
        yield
    finally:
        await disconnect_database()
        log.close()

        # Cancel all remaining tasks
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        [task.cancel() for task in tasks]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception) and not isinstance(result, asyncio.CancelledError):
                logs.error(f"Error During Shutdown, {result}")

app = FastAPI(
    debug=conf.DEBUG,
    title=conf.TITLE,
    version=conf.VERSION,
    lifespan=init,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(albums.router)
app.include_router(artists.router)
app.include_router(artwork.router)
app.include_router(stream.router)
app.include_router(tracks.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=conf.HOST,
        port=conf.PORT,
        reload=conf.DEBUG,
        log_level=conf.LOG_LEVEL,
        log_config=None,
    )