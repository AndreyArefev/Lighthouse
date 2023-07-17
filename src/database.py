from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import AsyncGenerator
from sqlalchemy import NullPool

from .config import DB_URL, TEST_DB_URL, MODE

if MODE == "TEST":
    DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DB_URL}"
    DATABASE_PARAMS = {"poolclass": NullPool}
    print(MODE)
else:
    DATABASE_URL = f"sqlite+aiosqlite:///{DB_URL}"
    DATABASE_PARAMS = {}


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL,
                             echo=True,
                             **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
