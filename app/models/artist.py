from sqlalchemy import Column, String
from app.core.database import Base

class Artist(Base):
    __tablename__ = 'artists'

    artist: str = Column(String, nullable=False)
    artist_id: str = Column(String(32), primary_key=True, nullable=False)
