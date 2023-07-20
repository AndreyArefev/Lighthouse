from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.Auth.jwt_settings import AuthJWT
from src.Auth.service import UserManager


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        authorize = AuthJWT()
        user = await UserManager.auth_user(username, password)
        if user and user.is_superuser:
            access_token = authorize.create_access_token(subject=user.username)
            request.session.update({"token": access_token})
        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        # Check the token in depth


authentication_backend = AdminAuth(secret_key="...")
