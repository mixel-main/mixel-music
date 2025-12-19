from fastapi import APIRouter
from app.api.albums import router as albums_router
from app.api.artists import router as artists_router
from app.api.artwork import router as artwork_router
from app.api.auth import router as auth_router
from app.api.server import router as server_router
from app.api.tracks import router as tracks_router
from app.api.users import router as users_router

api_router = APIRouter(prefix='/api')

api_router.include_router(albums_router)
api_router.include_router(artists_router)
api_router.include_router(artwork_router)
api_router.include_router(auth_router)
api_router.include_router(server_router)
api_router.include_router(tracks_router)
api_router.include_router(users_router)
