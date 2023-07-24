from datetime import datetime
from typing import AsyncGenerator
from redis import asyncio as aioredis

from sqlalchemy import NullPool, TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import DB_URL, MODE, TEST_DB_URL, REDIS_HOST, REDIS_PORT

if MODE == "TEST":
    DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DB_URL}"
    DATABASE_PARAMS = {"poolclass": NullPool}
    print(MODE)
else:
    DATABASE_URL = f"sqlite+aiosqlite:///{DB_URL}"
    DATABASE_PARAMS = {}


class Base(DeclarativeBase):
    type_annotation_map = {datetime: TIMESTAMP(timezone=True)}


engine = create_async_engine(DATABASE_URL,
                             echo=True,
                             **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)

redis = aioredis.from_url(f"redis://{REDIS_HOST}")

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_redis_connect():
    connection = aioredis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    yield connection
