import datetime

from jinja2 import Environment, FileSystemLoader
from jose import JWTError, jwt
from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError

from src.Auth.models import User
from src.Auth.schemas import SCreateUser
from src.Auth.utils import verify_password
from src.config import ALGORITHM, SECRET_KEY
from src.database import async_session_maker, get_async_session, redis as r
from src.exception import ExCredentials
from src.logger import logger



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
        #try:
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
        '''except (SQLAlchemyError, Exception) as error:
            if error == SQLAlchemyError:
                msg = 'Database exs:'
            else:
                msg = 'Unknown exs:'
            msg += ' Cannot add user'
            extra = {'user': user.username}
            logger.error(msg, extra=extra, exc_info=True)'''



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


class TokenManager:
    @classmethod
    async def create_tokens(cls, authorize, subject):
        access_token = await authorize.create_access_token(subject=subject)
        refresh_token = await authorize.create_refresh_token(subject=subject)
        await cls._set_refresh_token_in_redis(subject, refresh_token)
        await cls._set_tokens_in_cookies(authorize, access_token, refresh_token)
        return access_token, refresh_token

    @staticmethod
    async def _set_tokens_in_cookies(authorize, access_token, refresh_token):
        await authorize.set_access_cookies(access_token)
        await authorize.set_refresh_cookies(refresh_token)

    @staticmethod
    async def _set_refresh_token_in_redis(subject, refresh_token):
        async with r.pipeline(transaction=True) as pipe:
            await (pipe.set(refresh_token, subject).execute())

    @classmethod
    async def get_username_current_user_from_refresh_token(cls, authorize):
        await authorize.jwt_refresh_token_required()
        current_user = await authorize.get_jwt_subject()
        return current_user
