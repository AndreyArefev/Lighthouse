from datetime import timedelta
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings, BaseModel
import src.config as conf

class SSettings(BaseModel):
    """Настройки по созданию JWT токенов"""
    authjwt_access_token_expires: timedelta = conf.AUTHJWT_ACCESS_TOKEN_EXPIRES
    authjwt_refresh_token_expires: timedelta = conf.AUTHJWT_REFRESH_TOKEN_EXPIRES
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_secret_key: str = conf.SECRET_KEY
    authjwt_algorithm: str = conf.ALGORITHM
    authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
def get_config():
    return SSettings()
