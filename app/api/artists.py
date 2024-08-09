from fastapi import APIRouter, status, HTTPException, Query
from core.library import *
from infra.loggings import *

router = APIRouter(prefix = '/api')

@router.get('/artists')
async def api_artist_list(
    page: int = Query(1, ge=1),
    item: int = Query(40, ge=1),
) -> dict | list[dict]:

    artist_list = await Library.get_artist_list(page, item)
    return artist_list


@router.get('/artists/{hash}')
async def api_artist_info(
    hash: str,
) -> dict | list[dict]:

    artist_info = await Library.get_artist_info(hash)
    return artist_info