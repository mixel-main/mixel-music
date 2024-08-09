from infra.config import *
from PIL import Image
import io

async def save_artwork(artwork: bin, albumhash: str) -> None:
    artwork_path = conf.IMG_DIR
    orig_artwork = Image.open(io.BytesIO(artwork))
    suffix = orig_artwork.format.lower()

    if suffix is None: return
    # orig_artwork_path = artwork_path / f'{albumhash}_orig.{suffix}'
    # if not orig_artwork_path.exists():
    #     orig_artwork.save(orig_artwork_path.as_posix(), suffix)
        
    create_list = list(conf.IMG_SIZE)
    for file in artwork_path.iterdir():
        for size in conf.IMG_SIZE:
            if file.is_file() and file.name.endswith(f'{albumhash}_{size}.{conf.IMG_TYPE}'):
                create_list.remove(size)

    if create_list:
        for size in create_list:
            thumb_image = orig_artwork.copy()
            thumb_image.thumbnail([size, size], Image.Resampling.LANCZOS)
            thumb_image_name = (artwork_path / f'{albumhash}_{size}.{conf.IMG_TYPE}').as_posix()
            thumb_image.save(thumb_image_name, conf.IMG_TYPE, quality=conf.IMG_QUAL)