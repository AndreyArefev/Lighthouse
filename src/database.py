from datetime import datetime
from typing import AsyncGenerator
from redis import asyncio as aioredis

from sqlalchemy import NullPool, TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

import src.config as c

if c.MODE == "TEST":
    DATABASE_URL = f"postgresql+asyncpg://{c.TEST_DB_USER}:{c.TEST_DB_PASS}@{c.TEST_DB_HOST}:{c.TEST_DB_PORT}/{c.TEST_DB_NAME}"
    SQLITE_DATABASE_URL = f"ssqlite+aiosqlite:///{c.TEST_SQLITE_DB_URL}"
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = f"postgresql+asyncpg://{c.DB_USER}:{c.DB_PASS}@{c.DB_HOST}:{c.DB_PORT}/{c.DB_NAME}"
    SQLITE_DATABASE_URL = f"sqlite+aiosqlite:///{c.SQLITE_DB_URL}"
    DATABASE_PARAMS = {}

if c.DB == 'SQLITE':
    CURRENT_DATABASE_URL = SQLITE_DATABASE_URL
else:
    CURRENT_DATABASE_URL = DATABASE_URL

print(CURRENT_DATABASE_URL)

class Base(DeclarativeBase):
    type_annotation_map = {datetime: TIMESTAMP(timezone=True)}

engine = create_async_engine(CURRENT_DATABASE_URL,
                             echo=True,
                             **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)

redis = aioredis.from_url(f"redis://{c.REDIS_HOST}")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

