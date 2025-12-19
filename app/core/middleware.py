from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

class CustomSessionMiddleware(BaseHTTPMiddleware):
    ALLOWED_PATHS = (
        "/api/auth/signup",
        "/api/auth/signin",
        "/api/auth/logout",
        "/api/auth/ping",
    )

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if not path.startswith("/api") or path.startswith(self.ALLOWED_PATHS):
            return await call_next(request)

        session_id = request.cookies.get("session")
        if not session_id:
            return self._unauthorized_response()

        auth_service = request.app.state.auth_service
        user_id = auth_service.get_user_id(session_id)

        if not user_id:
            return self._unauthorized_response(clear_cookie=True)

        request.state.user_id = user_id

        return await call_next(request)

    @staticmethod
    def _unauthorized_response(clear_cookie: bool = False) -> Response:
        response = Response(status_code=status.HTTP_401_UNAUTHORIZED)
        if clear_cookie:
            response.delete_cookie("session")
        return response
