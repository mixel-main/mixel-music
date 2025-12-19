import uuid
from datetime import datetime, timezone
from typing import Any
from app.core.database import NoResultFound
from app.repos.user import UserRepo
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth import AuthService

class InvalidCredentials(Exception):
    pass

class AlreadyExists(Exception):
    pass

class UserService:
    def __init__(self, repo: UserRepo, auth: AuthService) -> None:
        self.repo = repo
        self.auth = auth

    async def list_users(self) -> tuple[list[dict[str, Any]], int]:
        return await self.repo.list_users()

    async def get_user(self, user_id: str) -> dict[str, Any]:
        return await self.repo.get_user(user_id)

    async def check_credential(self, email: str, password: str) -> str:
        hashed = await self.repo.get_password(email)
        if not hashed:
            raise InvalidCredentials

        if not self.auth.password_verify(hashed, password):
            raise InvalidCredentials

        user_id = await self.repo.get_user_id_from_email(email)
        if not user_id:
            raise InvalidCredentials

        return user_id

    async def update_last_login(self, user_id: str) -> None:
        await self.repo.update_user(
            user_id,
            {"last_login": datetime.now(timezone.utc)},
        )

    async def create_user(self, data: UserCreate) -> str:
        if await self.repo.is_user_exist(data.email):
            raise AlreadyExists

        user_id = str(uuid.uuid4())

        user_row = {
            "user_id": user_id,
            "email": data.email,
            "username": data.username,
            "password": self.auth.password_encode(data.password),
            "created_at": datetime.now(timezone.utc),
            "last_login": datetime(1970, 1, 1, tzinfo=timezone.utc),
            "role": "user",
            "profile_img": "",
            "preferences": {},
        }

        await self.repo.create_user(user_row)
        return user_id

    async def update_user(self, user_id: str, user_data: UserUpdate) -> None:
        if not await self.repo.is_user_exist(user_id):
            raise NoResultFound

        await self.repo.update_user(user_id, user_data.model_dump(exclude_unset=True))

    async def delete_user(self, user_id: str) -> None:
        if not await self.repo.is_user_exist(user_id):
            raise NoResultFound

        self.auth.delete_all_session(user_id)
        await self.repo.delete_user(user_id)
