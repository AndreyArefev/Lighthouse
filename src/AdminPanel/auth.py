from src.Auth.base_config import fastapi_users
from src.Auth.base_config import auth_backend
from src.Auth.models import User
from fastapi_users.authentication import AuthenticationBackend
from fastapi import Depends
from src.database import get_async_session
from src.Auth.service import get_user_db, CustomSQLAlchemyUserDatabase
from src.Auth.usermanager import get_user_manager
from typing import Optional
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse


class UserDate:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        print(username)
        adminusermanager=await anext(get_user_manager(await anext(get_user_db(await anext(get_async_session())))))
        userdate = UserDate(username, password)
        user = await adminusermanager.authenticate(credentials=userdate)
        print(user)
        if user:
            print(1)
            token = await adminusermanager.request_verify(user)
            print(token)
            print(2)
            request.session.update({"token": token})
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
