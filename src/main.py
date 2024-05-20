import time
import sentry_sdk

from fastapi import FastAPI, Request
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
from src.logger import logger

app = FastAPI(
    title='LighthouseAPI'
)

sentry_sdk.init(
    dsn="https://d80e3d565ed84f12b944f8c79ad0af64@o4505583956393984.ingest.sentry.io/4505583978676224"
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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info("Time execution request", extra={
        "process time": round(process_time, 4)
    })
    return response

