from fastapi import FastAPI
from src.database import engine
from sqladmin import Admin
from src.AdminPanel.views import UserAdmin, EventAdmin
from src.AdminPanel.auth import authentication_backend
from src.Events.router import router as event_router
from src.Auth.router import router as auth_router

app = FastAPI(
    title='LighthouseAPI'
)

app.include_router(auth_router)
app.include_router(event_router)


admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(EventAdmin)


