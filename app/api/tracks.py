from fastapi import APIRouter, status, HTTPException, Query
from core.library import *
from infra.loggings import *

router = APIRouter(prefix = '/api')

@router.get('/tracks')
async def api_track_list(
    page: int = Query(1, ge=1),
    item: int = Query(40, ge=1),
) -> dict | list[dict]:
    
    track_list = await Library.get_track_list(page, item)
    return track_list


@router.get('/tracks/{hash}')
async def api_track_info(
    hash: str,
) -> dict | list[dict]:

    track_info = await Library.get_track_info(hash)
    return track_info