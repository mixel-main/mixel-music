import asyncio
import io
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse, StreamingResponse, Response
from PIL import Image
from app.core.dependencies import get_library_repo
from app.repos.library import LibraryRepo
from app.services.artwork import ArtworkService

router = APIRouter(tags=['Artwork'])

def _render_thumbnail(
    data: bytes,
    size: int,
) -> tuple[bytes, str, Image.Image]:
    img = Image.open(io.BytesIO(data))
    fmt = (img.format or "jpeg").lower()

    img.thumbnail((size, size), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, fmt)

    return buf.getvalue(), fmt, img

@router.get("/artwork/{id}")
async def get_artwork(
    id: str,
    size: int = Query(300, ge=0),
    repo: LibraryRepo = Depends(get_library_repo),
) -> Response:
    service = ArtworkService(repo)

    cached_path = await service.get_artwork(id, size)
    if cached_path:
        return FileResponse(cached_path)

    data: Optional[bytes] = await service.init_artwork(id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if size == 0:
        return StreamingResponse(io.BytesIO(data), media_type="application/octet-stream")

    loop = asyncio.get_running_loop()
    thumb_bytes, fmt, img = await loop.run_in_executor(service.executor, _render_thumbnail, data, size)

    await loop.run_in_executor(service.executor, service.save_artwork, img, id, size, fmt)

    return StreamingResponse(io.BytesIO(thumb_bytes), media_type=f"image/{fmt}")
