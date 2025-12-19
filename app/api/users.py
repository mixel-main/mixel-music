from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import NoResultFound
from app.core.dependencies import get_user_service
from app.schemas.user import UserDetail, UserListResponse, UserUpdate
from app.services.user import UserService

router = APIRouter(tags=['Users'])

@router.get(
    "/users",
    response_model=UserListResponse,
)
async def list_users(
    service: UserService = Depends(get_user_service),
) -> UserListResponse:
    users, total = await service.list_users()
    
    return {
        "items": users,
        "total": total
    }

@router.get(
    "/users/{id}",
    response_model=UserDetail,
)
async def get_user(
    id: str,
    service: UserService = Depends(get_user_service),
) -> UserDetail:
    try:
        return await service.get_user(id)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.put(
    "/users/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_user(
    id: str,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> None:
    try:
        await service.update_user(id, user_data)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.delete(
    "/users/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    id: str,
    service: UserService = Depends(get_user_service),
) -> None:
    try:
        await service.delete_user(id)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
