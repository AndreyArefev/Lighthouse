from typing import Annotated
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.Auth.service import UserManager
from src.Auth.models import User
from src.exception import ExCredentials, ExInactiveUser, ExNotAdmin, ExTokenExpired
from src.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_token(request: Request) -> str:
    """Получение токена из куков"""
    token = request.cookies.get("access_token")
    if not token:
        raise ExTokenExpired
    return token


async def get_current_user(token: str = Depends(get_token),
                           usermanager: UserManager = Depends()) -> User:
    """Получение текущего пользователя по его токену"""
    username = await usermanager.get_username_from_token(token=token)
    user = await usermanager.find_user_one_or_none(username=username)
    print('!@#')
    if user is None:
        raise ExCredentials
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """Проверка что пользователь имеет доступ"""
    if not current_user.is_active:
        raise ExInactiveUser
    return current_user


async def get_current_superuser(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """Проверка что пользователь админ"""
    if not current_user.is_superuser:
        raise ExNotAdmin
    return current_user



