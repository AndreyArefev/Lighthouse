from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.Auth.service import UserManager
from src.Auth.models import User
from src.exception import ExceptionCredentials
from src.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_token(request: Request) -> str:
    """Получение токена из куков"""
    token = request.cookies.get("access_token")
    if not token:
        raise ExceptionCredentials
    return token


async def get_current_user(token: str = Depends(get_token),
                           usermanager: UserManager = Depends()) -> User:
    """Получение текущего пользователя по его токену"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise ExceptionCredentials
    except JWTError:
        raise ExceptionCredentials
    user = await usermanager.find_user_one_or_none(username=username)
    if user is None:
        raise ExceptionCredentials
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """Проверка что пользователь имеет доступ"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
