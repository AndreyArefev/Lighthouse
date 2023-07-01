from fastapi import FastAPI, APIRouter, Query
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from src.Auth.models import User
from src.Auth.schemas import UserRead, UserCreate
from src.Auth.usermanager import get_user_manager
from src.Auth.base_config import auth_backend
from src.Events.router import router as event_router
from src.Auth.base_config import fastapi_users
from src.database import engine
from sqladmin import Admin, ModelView
from src.AdminPanel.views import UserAdmin, EventAdmin
from src.AdminPanel.auth import authentication_backend

app = FastAPI(
    title='LighthouseAPI'
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    event_router,
    prefix="/events",
    tags=['Events'],
)


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(EventAdmin)
