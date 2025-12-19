from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.core.database import NoResultFound
from app.core.dependencies import get_library_service
from app.schemas.artist import ArtistDetail, ArtistListResponse
from app.services.library import LibraryService

router = APIRouter(tags=['Artists'])

@router.get("/artists", response_model=ArtistListResponse)
async def list_artists(
    offset: int = Query(0, ge=0),
    limit: int = Query(40, ge=1, le=200),
    service: LibraryService = Depends(get_library_service),
) -> ArtistListResponse:
    try:
        items, total = await service.list_artists(offset=offset, limit=limit)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return {
        "items": items,
        "total": total,
    }

@router.get("/artists/{id}", response_model=ArtistDetail)
async def get_artist(
    id: str,
    service: LibraryService = Depends(get_library_service),
) -> ArtistDetail:
    try:
        return await service.get_artist(id)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
