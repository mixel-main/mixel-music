from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, REAL, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Artist(Base):
    __tablename__ = "artists"
    artist: Mapped[str] = mapped_column(String, nullable=False)
    artist_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, nullable=False)
    artistsort: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False
    )
    missing: Mapped[bool] = mapped_column(Boolean, nullable=False)
    musicbrainz_artistid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False
    )