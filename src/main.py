from fastapi import FastAPI
from src.database import engine
from sqladmin import Admin
from src.AdminPanel.views import UserAdmin, EventAdmin
from src.AdminPanel.auth import authentication_backend
from src.Events.router import router as event_router
from src.Auth.router import router as auth_router
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

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


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

