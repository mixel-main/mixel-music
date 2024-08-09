from fastapi import APIRouter, Header, status, Response, HTTPException
from core.library import *
from infra.loggings import *

router = APIRouter(prefix = '/api')

@router.get('/stream/{hash}')
async def api_stream(
    hash: str,
    range: str = Header(None),
) -> Response:

    stream_content, stream_headers = await Library.streaming(hash, range)
    if stream_content:
        return Response(
            content=stream_content,
            headers=stream_headers,
            status_code=status.HTTP_206_PARTIAL_CONTENT
        )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)