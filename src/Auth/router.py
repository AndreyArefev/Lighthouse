from fastapi import FastAPI, HTTPException, Depends, Request, Response, APIRouter
from src.Auth.schemas import SCreateUser
from src.Auth.jwt_settings import AuthJWT
import src.exception as ex
from src.Auth.utils import get_password_hash
from src.Auth.service import UserManager
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация"]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register")
async def register_user(user_date: SCreateUser, usermanager: UserManager = Depends()):
    if await usermanager.find_user_one_or_none(username=user_date.username):
        raise ex.ExceptionUsernameAlreadyExists
    if await usermanager.find_user_one_or_none(email=user_date.email):
        raise ex.ExceptionEmailAlreadyExists
    user_date.password = get_password_hash(user_date.password)
    await usermanager.create_user(user_date)


@router.post('/login')
async def login(response: Response,
          form_data: OAuth2PasswordRequestForm = Depends(),
          authorize: AuthJWT = Depends(),
          usermanager: UserManager = Depends()):
    user = await usermanager.auth_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Логин или пароль неверны')
    if not user.is_verified:
        raise HTTPException(status_code=401, detail='Верифицируйте свой email, перейдя по сслыке в полученном письме')
    access_token = authorize.create_access_token(subject=form_data.username)
    refresh_token = authorize.create_refresh_token(subject=form_data.username)
    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)
    #response.set_cookie("access_token", access_token, httponly=True)
    #response.set_cookie("csrf_refresh_token", refresh_token, httponly=True)
    #response.set_cookie('logged_in', 'True')
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post('/refresh')
def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)
    authorize.set_access_cookies(new_access_token)
    return {"access_token": new_access_token}

@router.get('/protected')
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}

@router.get('/logout')
def logout(response: Response,
           authorize: AuthJWT = Depends()):
           #user_id: str = Depends(oauth2.require_user)):
    authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}




