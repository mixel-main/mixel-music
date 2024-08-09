from pydantic_settings import BaseSettings
from tools.path_handler import *
import logging

class Config(BaseSettings):
    TITLE: str = 'mixel-music'
    VERSION: str = '0.4.0'
    HOST: str = '0.0.0.0'
    PORT: int = 2843

    DB_URL: str = "sqlite+aiosqlite:///" \
        + str_path('config', 'mixel-music.db', rel=False)
    I18N_DIR: Path = get_path('i18n')
    DATA_DIR: Path = get_path('config')
    LOG_PATH: Path = get_path('config', 'mixel-music.txt')
    MUSIC_DIR: Path = get_path('library')

    IMG_DIR: Path = get_path('config', 'artworks')
    IMG_SIZE: list[int] = [128, 300, 500]
    IMG_TYPE: str = 'webp' # png, jpeg, webp
    IMG_QUAL: int = 100

    LOG_LEVEL: int = logging.DEBUG
    DB_ECHO: bool = False
    DEBUG: bool = True

conf = Config()