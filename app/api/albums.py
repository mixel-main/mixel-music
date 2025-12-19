from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.core.database import NoResultFound
from app.core.dependencies import get_library_service
from app.schemas.album import AlbumDetail, AlbumListResponse
from app.services.library import LibraryService

router = APIRouter(tags=['Albums'])

@router.get("/albums", response_model=AlbumListResponse)
async def list_albums(
    offset: int = Query(0, ge=0),
    limit: int = Query(40, ge=1),
    service: LibraryService = Depends(get_library_service),
) -> AlbumListResponse:
    try:
        items, total = await service.list_albums(offset, limit)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return {
        "items": items,
        "total": total,
    }

@router.get("/albums/{id}", response_model=AlbumDetail)
async def get_album(
    id: str,
    service: LibraryService = Depends(get_library_service),
) -> AlbumDetail:
    try:
        return await service.get_album(id)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
