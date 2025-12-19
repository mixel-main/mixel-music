from datetime import datetime, timezone
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    REAL,
    String,
    Text,
)
from app.core.database import Base

class Track(Base):
    __tablename__ = 'tracks'

    album: str = Column(String, ForeignKey('albums.album'), nullable=False)
    album_id: str = Column(String(32), nullable=False)
    albumartist: str = Column(String, nullable=False)
    albumartist_id: str = Column(String(32), nullable=False)
    artist: str = Column(String, nullable=False)
    artist_id: str = Column(String(32), nullable=False)
    barcode: str = Column(String, nullable=False)
    bitdepth: int = Column(Integer, nullable=False)
    bitrate: float = Column(REAL, nullable=False)
    channels: int = Column(Integer, nullable=False)
    compilation: bool = Column(Boolean, nullable=False)
    comment: str = Column(String, nullable=False)
    composer: str = Column(String, nullable=False)
    content_type: str = Column(String, nullable=False)
    copyright: str = Column(String, nullable=False)
    created_at: DateTime = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False
    )
    date: str = Column(String, nullable=False)
    director: str = Column(String, nullable=False)
    directory: str = Column(String, nullable=False)
    duration: float = Column(REAL, nullable=False)
    disc_number: int = Column(Integer, nullable=False)
    disc_total: int = Column(Integer, nullable=False)
    filepath: str = Column(String, nullable=False)
    filesize: int = Column(Integer, nullable=False)
    genre: str = Column(String, nullable=False)
    isrc: str = Column(String(12), nullable=False)
    label: str = Column(String, nullable=False)
    lyrics: str = Column(Text, nullable=False)
    samplerate: int = Column(Integer, nullable=False)
    title: str = Column(String, nullable=False)
    track_id: str = Column(String(32), primary_key=True, nullable=False)
    track_number: int = Column(Integer, nullable=False)
    track_total: int = Column(Integer, nullable=False)
    updated_at: DateTime = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False
    )
    year: int = Column(Integer, nullable=False)
