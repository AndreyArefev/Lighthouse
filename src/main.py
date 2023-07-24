from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin

from src.AdminPanel.auth import authentication_backend
from src.AdminPanel.views import EventAdmin, UserAdmin, CategoryAdmin, TagAdmin
from src.Auth.router import router as auth_router
from src.config import REDIS_HOST
from src.database import engine
from src.database import redis
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
admin.add_view(CategoryAdmin)
admin.add_view(TagAdmin)


@app.on_event("startup")
async def startup():
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

