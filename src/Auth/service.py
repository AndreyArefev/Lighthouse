import datetime
from sqlalchemy import select, insert, update
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.Auth.models import User
from src.Auth.schemas import SCreateUser
from src.database import get_async_session, async_session_maker
from src.Auth.utils import verify_password
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from src.Auth.models import User
from src.exception import ExCredentials
from src.config import SECRET_KEY, ALGORITHM
from jinja2 import Environment, FileSystemLoader


class UserManager:
    """Класс отвечающий за работу с пользователями"""

    @classmethod
    async def find_user_one_or_none(cls, **filter) -> User | None:
        """Функция поиска пользователя по фильтру"""
        async with async_session_maker() as session:
            statement = select(User).filter_by(**filter)
            result = await session.execute(statement)
            return result.scalar_one_or_none()

    @classmethod
    async def create_user(cls, user: SCreateUser) -> User:
        async with async_session_maker() as session:
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

    @classmethod
    async def auth_user(cls, username: str, password: str) -> User | None:
        "Аутентификация пользователя"
        user = await cls.find_user_one_or_none(username=username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @classmethod
    async def verified_user(cls, token: str) -> str:
        "Верификация пользователя"
        username = await cls.get_username_from_token(token=token)
        await cls._install_status_verification_in_true(username)
        environment = Environment(loader=FileSystemLoader("src/Templates/"))
        template = environment.get_template("page_verification_confirmations.html").render(username=username)
        return template

    @classmethod
    async def _install_status_verification_in_true(cls, username):
        "Установка флага верификации пользователя в True"
        async with async_session_maker() as session:
            statement = update(User).where(User.username == username).values(is_verified=True)
            await session.execute(statement)
            await session.commit()


    @staticmethod
    async def get_username_from_token(token: str):
        "Получение имени пользователя из токена"
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise ExCredentials
            return username
        except JWTError:
            raise ExCredentials
