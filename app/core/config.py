import tomllib
from functools import cached_property, lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.path import get_path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # app
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 2843

    # dir
    DATA_DIR: Path = Field(default_factory=lambda: get_path("data"))
    LIBRARY_DIR: Path = Field(default_factory=lambda: get_path("music"))
    ARTWORK_DIR: Path = Field(default_factory=lambda: get_path("data", "artworks"))
    LOG_PATH: Path = Field(default_factory=lambda: get_path("data", "mixel-music.log"))

    # log
    LOG_LEVEL: str = "DEBUG"

    # artwork
    ARTWORK_FORMAT: str = "webp"
    ARTWORK_CACHING: bool = True
    ARTWORK_QUALITY: int = 100
    ARTWORK_TARGETS: set[str] = {".png", ".jpg", ".jpeg", ".tiff"}

    @cached_property
    def DB_URL(self) -> str:
        db_path = get_path(self.DATA_DIR, 'mixel-music.db', rel=False)
        return f"sqlite+aiosqlite:///{db_path.as_posix()}"
    
    @cached_property
    def VERSION(self) -> str:
        pyproject = get_path("pyproject.toml", rel=False)
        try:
            with pyproject.open("rb") as f:
                data = tomllib.load(f)
            return str(data["tool"]["poetry"]["version"])
        except Exception:
            return "0.0.0"


def ensure_dirs() -> None:
    config = get_config()

    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    config.LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    config.ARTWORK_DIR.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_config() -> Settings:
    return Settings()
