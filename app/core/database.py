from contextlib import asynccontextmanager
from fastapi import HTTPException
from typing import AsyncGenerator
from sqlalchemy import text, func, select, insert, update, delete, or_, and_, join, exists
from sqlalchemy.dialects.sqlite import Insert
from sqlalchemy.exc import OperationalError, SQLAlchemyError, DatabaseError, NoResultFound
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import get_config
from app.core.logger import get_logger

logger = get_logger()
config = get_config()

Base = declarative_base()
engine = create_async_engine(config.DB_URL)

session = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@asynccontextmanager
async def db_conn() -> AsyncGenerator[AsyncSession, None]:
    async with session() as conn:
        try:
            yield conn
            await conn.commit()

        except Exception as error:
            if not isinstance(error, HTTPException):
                logger.error("Error occurred: %s", error)
                await conn.rollback()
            raise

async def connect_database() -> None:
    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        await conn.execute(text("PRAGMA busy_timeout=5000;"))
        await conn.run_sync(Base.metadata.create_all)

async def disconnect_database() -> None:
    await engine.dispose()
