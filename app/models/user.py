from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, JSON, String
from app.core.database import Base

class User(Base):
    __tablename__ = 'users'

    user_id: str = Column(String, primary_key=True, nullable=False)
    email: str = Column(String, nullable=False)
    username: str = Column(String, nullable=False)
    password: str = Column(String, nullable=False)
    last_login: DateTime = Column(DateTime, nullable=False)
    created_at: DateTime = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    role: str = Column(String, nullable=False)
    profile_img: str = Column(String, nullable=False)
    preferences: str = Column(JSON, nullable=False)
