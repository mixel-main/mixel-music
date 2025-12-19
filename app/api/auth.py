from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from app.core.dependencies import get_user_service, get_auth_service
from app.schemas.user import UserCreate, UserSignin
from app.services.user import UserService, InvalidCredentials
from app.services.auth import AuthService

router = APIRouter(tags=["Auth"])

COOKIE_NAME = "session"
SESSION_MAX_AGE = 60 * 60 * 24 * 28 # 28 days

@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    response: Response,
    auth: AuthService = Depends(get_auth_service),
) -> None:
    session_id = request.cookies.get(COOKIE_NAME)
    if session_id:
        auth.delete_session(session_id)

    response.delete_cookie(key=COOKIE_NAME)

@router.post("/auth/signin", status_code=status.HTTP_204_NO_CONTENT)
async def signin(
    form: UserSignin,
    response: Response,
    service: UserService = Depends(get_user_service),
    auth: AuthService = Depends(get_auth_service),
) -> None:
    try:
        user_id = await service.check_credential(form.email, form.password)
    except InvalidCredentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    session_id = auth.create_session(user_id)
    await service.update_last_login(user_id)

    response.set_cookie(
        key=COOKIE_NAME,
        value=session_id,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=SESSION_MAX_AGE,
    )

@router.post("/auth/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    form: UserCreate,
    service: UserService = Depends(get_user_service),
) -> None:
    await service.create_user(form)
