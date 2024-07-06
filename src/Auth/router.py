from fastapi import APIRouter, Depends, HTTPException, Response, Request, Header
from src.database import redis as r
import src.exception as ex
from src.Auth.jwt_settings import AuthJWT
from src.Auth.schemas import SAuthUser, SCreateUser
from src.Auth.service import UserManager, TokenManager
from src.Auth.utils import create_confirm_token, get_password_hash
from src.Tasks.tasks import send_verified_email
from src.config import AUTHJWT_ACCESS_TOKEN_EXPIRES


router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация"]
)


@router.post("/register")
async def register_user(user_date: SCreateUser):
    username = await UserManager.find_user_one_or_none(username=user_date.username)
    email = await UserManager.find_user_one_or_none(email=user_date.email)
    if username:
        raise ex.ExUsernameAlreadyExists
    if email:
        raise ex.ExEmailAlreadyExists
    user_date.password = get_password_hash(user_date.password)
    confirm_token = create_confirm_token(user_date.username)
    send_verified_email.delay(user_date.email, confirm_token)
    new_user = await UserManager.create_user(user_date)
    return new_user


@router.post('/login')
async def login(form_data: SAuthUser,
                authorize: AuthJWT = Depends()):
    user = await UserManager.auth_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Логин или пароль неверны')
    if not user.is_verified:
        raise HTTPException(status_code=401, detail='Верифицируйте свой email, перейдя по сслыке в полученном письме')
    access_token, refresh_token = await TokenManager.create_tokens(authorize, user.username)
    return {"access_token": access_token, "access_token_expires": AUTHJWT_ACCESS_TOKEN_EXPIRES, "refresh_token": refresh_token}


@router.get('/verification/')
async def verification(token: str):
    template = await UserManager.verified_user(token)
    return template

@router.post('/refresh')
async def refresh(request: Request,
                  authorize: AuthJWT = Depends(),
                  authorization: str = Header(None, convert_underscores=False)):
    if authorization is None or not authorization.startswith("Bearer "):
        return {"error": "Invalid Authorization header format. Please provide a Bearer token."}
    refresh_token = authorization.split(" ")[1]
    if refresh_token and await r.get(refresh_token):
        current_user = await TokenManager.get_username_current_user_from_refresh_token(authorize)
        new_access_token = await TokenManager.create_access_token(authorize, current_user)
        return {"access_token": new_access_token, "access_token_expires": AUTHJWT_ACCESS_TOKEN_EXPIRES}


@router.get('/logout')
async def logout(request: Request,
                 authorize: AuthJWT = Depends()):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        await r.delete(refresh_token)
        await authorize.unset_jwt_cookies()
        return {'status': 'success'}
    else:
        return {'status': 'error'}











