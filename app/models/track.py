from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, REAL, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Track(Base):
    __tablename__ = "tracks"
    album: Mapped[str] = mapped_column(String, ForeignKey('albums.album'), nullable=False)
    album_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    albumartist: Mapped[str] = mapped_column(String, nullable=False)
    albumartist_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    albumartistsort: Mapped[str] = mapped_column(String, nullable=False)
    albumsort: Mapped[str] = mapped_column(String, nullable=False)
    artist: Mapped[str] = mapped_column(String, nullable=False)
    artist_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    artistsort: Mapped[str] = mapped_column(String, nullable=False)
    barcode: Mapped[str] = mapped_column(String, nullable=False)
    bitdepth: Mapped[int] = mapped_column(Integer, nullable=False)
    bitrate: Mapped[float] = mapped_column(REAL, nullable=False)
    channels: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(String, nullable=False)
    compilation: Mapped[bool] = mapped_column(Boolean, nullable=False) 
    composer: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    copyright: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False
    ) # s
    date: Mapped[str] = mapped_column(String, nullable=False)
    discnumber: Mapped[int] = mapped_column(Integer, nullable=False)
    duration: Mapped[float] = mapped_column(REAL, nullable=False)
    filepath: Mapped[str] = mapped_column(String, nullable=False)
    filesize: Mapped[float] = mapped_column(REAL, nullable=False)
    genre: Mapped[str] = mapped_column(String, nullable=False)
    isrc: Mapped[str] = mapped_column(String(12), nullable=False)
    label: Mapped[str] = mapped_column(String, nullable=False)
    lyrics: Mapped[str] = mapped_column(Text, nullable=False)
    missing: Mapped[bool] = mapped_column(Boolean, nullable=False) # s
    musicbrainz_albumartistid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    musicbrainz_albumid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    musicbrainz_artistid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    musicbrainz_discid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    musicbrainz_originalalbumid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    musicbrainz_originalartistid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    musicbrainz_recordingid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    musicbrainz_releasegroupid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    musicbrainz_trackid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    musicbrainz_workid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    participants: Mapped[JSON] = mapped_column(JSON, nullable=False)
    releasecountry: Mapped[str] = mapped_column(String, nullable=False)
    samplerate: Mapped[int] = mapped_column(Integer, nullable=False)
    subtitle: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    titlesort: Mapped[str] = mapped_column(String, nullable=False)
    totaldiscs: Mapped[int] = mapped_column(Integer, nullable=False)
    totaltracks: Mapped[int] = mapped_column(Integer, nullable=False)
    track_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, nullable=False)
    tracknumber: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False
    ) # s
    year: Mapped[int] = mapped_column(Integer, nullable=False)
