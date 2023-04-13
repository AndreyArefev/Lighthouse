from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from dotenv import load_dotenv
from src.database import async_session_maker
from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select
from src.Auth.models import User
from fastapi_users.db import BaseUserDatabase
from src.database import get_async_session
import os

load_dotenv()

PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=PRIVATE_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield CustomSQLAlchemyUserDatabase(session, User)


class CustomSQLAlchemyUserDatabase(SQLAlchemyUserDatabase):
    async def get_by_username(self, username: str):
        statement = select(self.user_table).where(
            self.user_table.username == username
        )
        return await self._get_user(statement.limit(1))

