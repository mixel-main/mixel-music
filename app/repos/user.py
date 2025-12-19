from typing import Any
from app.core.database import (
    AsyncConnection, select, insert, update, delete, func, NoResultFound
)
from app.models import User

class UserRepo:
    def __init__(self, conn: AsyncConnection) -> None:
        self.conn = conn

    async def get_user_id_from_email(self, email: str) -> str | None:
        if not email: return None

        query = await self.conn.execute(
            select(User.user_id).where(User.email == email)
        )
        result = query.mappings().first()
        return result.user_id if result.user_id else None
    
    async def is_user_exist(self, user_id: str) -> bool:
        if not user_id: return False

        query = await self.conn.execute(
            select(User).where(User.user_id == user_id)
        )
        result = query.mappings().first()
        return True if result else False

    async def get_password(self, email: str) -> str | None:
        query = await self.conn.execute(
            select(User.password).where(User.email == email)
        )
        result = query.mappings().first()
        return None if result is None else result.get('password')

    async def list_users(self) -> dict[str, Any]:
        users_query = await self.conn.execute(select(User.__table__))
        users = users_query.mappings().all()

        total_query = await self.conn.execute(
            select(func.count()).select_from(User)
        )
        total_query = total_query.scalar_one()
        return users, total_query

    async def get_user(self, user_id: str) -> dict[str, Any]:
        user_item = {}
        db_query = await self.conn.execute(
            select(User.__table__).where(User.user_id == user_id)
        )
        user_item = db_query.mappings().first()

        if user_item:
            return dict(user_item)
        else:
            raise NoResultFound
    
    async def create_user(self, user_data: dict[str, Any]) -> None:
        await self.conn.execute(
            insert(User).values(**user_data)
        )

    async def update_user(self, user_id: str, user_data: dict[str, Any]) -> None:
        await self.conn.execute(
            update(User).values(**user_data).where(User.user_id == user_id)
        )
    
    async def delete_user(self, user_id: str) -> None:
        await self.conn.execute(
            delete(User).where(User.user_id == user_id)
        )
