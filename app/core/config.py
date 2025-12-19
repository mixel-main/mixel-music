import tomllib
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.utils.path import get_path

class ConfigData(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    APP_NAME: str = "mixel-music"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 2843

    DATA_DIR: Path = Field(default_factory=lambda: get_path("data"))
    LIBRARY_DIR: Path = Field(default_factory=lambda: get_path("music"))
    ARTWORK_DIR: Path = Field(default_factory=lambda: get_path("data", "artworks"))
    LOG_PATH: Path = Field(default_factory=lambda: get_path("data", "mixel-music.log"))

    LOG_LEVEL: str = "DEBUG"

    ARTWORK_FORMAT: str = "webp"
    ARTWORK_CACHING: bool = True
    ARTWORK_QUALITY: int = 100
    ARTWORK_TARGETS: set[str] = {".png", ".jpg", ".jpeg", ".tiff"}


    @property
    def DB_URL(self) -> str:
        db_path = get_path(self.DATA_DIR, "database.db", rel=False)
        return f"sqlite+aiosqlite:///{db_path.as_posix()}"
    

    @property
    def VERSION(self) -> str:
        return get_app_version(self.APP_NAME, get_path("pyproject.toml", rel=False))

def get_poetry_version(path: Path) -> str:
    try:
        with path.open("rb") as f:
            data = tomllib.load(f)
        return data["tool"]["poetry"]["version"]
    except Exception:
        return "0.0.0"

def get_app_version(name: str, path: Path) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return get_poetry_version(path)

def get_config() -> ConfigData:
    return ConfigData()
