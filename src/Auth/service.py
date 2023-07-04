import datetime
from sqlalchemy import select
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.Auth.models import User
from src.Auth.schemas import SCreateUser
from src.database import get_async_session
from src.Auth.utils import verify_password



class UserManager:
    """Класс отвечающий за работу с пользователями"""
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def find_user_one_or_none(self, **filter) -> User | None:
        """Функция поиска пользователя по фильтру"""
        async with self.session as session:
            statement = select(User).filter_by(**filter)
            result = await session.execute(statement)
            return result.scalar_one_or_none()

    async def create_user(self, user: SCreateUser) -> User:
        async with self.session as session:
            new_user = User(email=user.email,
                            username=user.username,
                            phone=user.phone,
                            image=user.image,
                            registered_at=datetime.date.today(),
                            hashed_password=user.password,
                            is_active=True,
                            is_superuser=False,
                            is_verified=False
                            )
            session.add(new_user)
            await session.commit()
            return new_user

    async def auth_user(self, username: str, password: str) -> User | None:
        user = await self.find_user_one_or_none(username=username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
