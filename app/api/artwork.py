from fastapi import APIRouter, status, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse

from core.library import *
from tools.convert_value import *

router = APIRouter(prefix = '/api')

@router.get('/artwork/{hash}')
async def api_artwork(
    hash: str,
    bg_task: BackgroundTasks,
    type: int = 300,
):

    artwork_path = await Library.get_artwork(hash, type)

    try:
        return FileResponse(artwork_path)
    except:
        bg_task.add_task(gen_artwork, hash)
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={'message': 'extracting...'}
        )
    

async def gen_artwork(
    hash: str,
) -> None:
    
    await LibraryTask.create_artwork(hash)