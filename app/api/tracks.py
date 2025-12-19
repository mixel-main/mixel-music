from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response, status
from fastapi.responses import FileResponse
from app.core.database import NoResultFound
from app.core.dependencies import get_library_service, get_library_repo
from app.schemas.track import TrackDetail, TrackListResponse
from app.services.library import LibraryService
from app.utils.path import get_filename, get_path

router = APIRouter(tags=['Tracks'])

@router.get("/tracks", response_model=TrackListResponse)
async def list_tracks(
    offset: int = Query(0, ge=0),
    limit: int = Query(40, ge=1, le=200),
    service: LibraryService = Depends(get_library_service),
) -> TrackListResponse:
    try:
        items, total = await service.list_tracks(offset=offset, limit=limit)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return {
        "items": items,
        "total": total,
    }

@router.get("/tracks/{id}", response_model=TrackDetail)
async def get_track(
    id: str,
    service: LibraryService = Depends(get_library_service),
) -> TrackDetail:
    try:
        return await service.get_track(id)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.get('/tracks/{id}/stream')
async def stream(
    id: str,
    range: str = Header(None),
    service: LibraryService = Depends(get_library_service),
) -> Response:
    content, headers = await service.stream_track(id, range)

    return Response(
        content=content,
        headers=headers,
        status_code=status.HTTP_206_PARTIAL_CONTENT
    )

@router.get('/tracks/{id}/download')
async def download(
    track_id: str,
    service: get_library_repo = Depends(),
) -> FileResponse:    
    file_info = await service.get_track(track_id)

    return FileResponse(
        path=get_path(file_info.get('filepath')),
        filename=get_filename(file_info.get('filepath'))[0]
    )
