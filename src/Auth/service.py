from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import select
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.Auth.models import User
from src.database import get_async_session


class CustomSQLAlchemyUserDatabase(SQLAlchemyUserDatabase):
    async def get_by_username(self, username: str):
        statement = select(self.user_table).where(
            self.user_table.username == username
        )
        return await self._get_user(statement.limit(1))


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield CustomSQLAlchemyUserDatabase(session, User)
