from fastapi import Depends, Request
from app.core.database import AsyncGenerator, db_conn
from app.services.library import LibraryService
from app.services.user import UserService
from app.repos.library import LibraryRepo
from app.repos.user import UserRepo

async def get_library_repo() -> AsyncGenerator[LibraryRepo, None]:
    async with db_conn() as conn:
        yield LibraryRepo(conn)

async def get_library_service(
    repo: LibraryRepo = Depends(get_library_repo)
) -> LibraryService:
    return LibraryService(repo)

async def get_auth_service(request: Request):
    return request.app.state.auth_service

async def get_user_repo() -> AsyncGenerator[UserRepo, None]:
    async with db_conn() as conn:
        yield UserRepo(conn)

async def get_user_service(
    repo: UserRepo = Depends(get_user_repo),
    auth = Depends(get_auth_service),
) -> UserService:
    return UserService(repo, auth)
