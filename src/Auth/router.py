from fastapi import HTTPException, Depends, Response, APIRouter
from src.Auth.schemas import SCreateUser
from src.Auth.jwt_settings import AuthJWT
import src.exception as ex
from src.Auth.utils import get_password_hash, create_confirm_token
from src.Auth.service import UserManager
from fastapi.security import OAuth2PasswordRequestForm
from src.Tasks.tasks import send_verified_email
from src.Auth.dependencies import get_current_user
from src.Auth.models import User


router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация"]
)


@router.post("/register")
async def register_user(user_date: SCreateUser,
                        usermanager: UserManager = Depends()):
    if await usermanager.find_user_one_or_none(username=user_date.username):
        raise ex.ExUsernameAlreadyExists
    if await usermanager.find_user_one_or_none(email=user_date.email):
        raise ex.ExEmailAlreadyExists
    user_date.password = get_password_hash(user_date.password)
    confirm_token = create_confirm_token(user_date.username)
    send_verified_email.delay(user_date.email, confirm_token)
    await usermanager.create_user(user_date)


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
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
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get('/verification/')
async def verification(token: str,
                       usermanager: UserManager = Depends()):
    template = await usermanager.verified_user(token)
    return template


@router.post('/refresh')
async def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)
    authorize.set_access_cookies(new_access_token)
    return {"access_token": new_access_token}


@router.get('/logout')
async def logout(authorize: AuthJWT = Depends()):
    authorize.unset_jwt_cookies()
    return {'status': 'success'}
