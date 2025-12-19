from typing import Literal
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(tags=['Server'])

@router.get('/server/ping',
    response_class=PlainTextResponse,
    responses={
        200: {
            "content": {"text/plain": {"example": "pong"}}
        },
    }
)
async def ping() -> Literal['pong']:
    return 'pong'
