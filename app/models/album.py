from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, REAL, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Album(Base):
    __tablename__ = "albums"
    album: Mapped[str] = mapped_column(String, nullable=False)
    album_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, nullable=False)
    albumartist: Mapped[str] = mapped_column(String, nullable=False)
    albumartist_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    albumartistsort: Mapped[str] = mapped_column(String, nullable=False)
    albumsort: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False
    )
    max_year: Mapped[int] = mapped_column(Integer, nullable=False)
    min_year: Mapped[int] = mapped_column(Integer, nullable=False)
    missing: Mapped[bool] = mapped_column(Boolean, nullable=False)
    musicbrainz_albumartistid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    musicbrainz_albumid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    totaldiscs: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False
    )