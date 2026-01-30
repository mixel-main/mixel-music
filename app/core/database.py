from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_config
from app.core.logger import get_logger

logger = get_logger(__name__)
config = get_config()


class Base(AsyncAttrs, DeclarativeBase):
    pass


engine: AsyncEngine | None = None
SessionLocal: async_sessionmaker[AsyncSession] | None = None


@asynccontextmanager
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    if SessionLocal is None:
        raise RuntimeError

    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def connect_db() -> None:
    global engine, SessionLocal
    if engine is not None:
        return

    config = get_config()

    engine = create_async_engine(
        config.DB_URL,
        echo=False,
        future=True,
    )

    SessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    import app.models

    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        await conn.execute(text("PRAGMA busy_timeout=5000;"))
        await conn.execute(text("PRAGMA synchronous=NORMAL;"))
        await conn.run_sync(Base.metadata.create_all)


async def disconnect_db() -> None:
    global engine, SessionLocal
    if engine is None:
        return
    
    await engine.dispose()

    engine = None
    SessionLocal = None
