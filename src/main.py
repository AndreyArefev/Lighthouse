from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from src.AdminPanel.auth import authentication_backend
from src.AdminPanel.views import EventAdmin, UserAdmin
from src.Auth.router import router as auth_router
from src.config import REDIS_HOST
from src.database import engine
from src.Events.router import router as event_router

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
    redis = aioredis.from_url(f"redis://{REDIS_HOST}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

