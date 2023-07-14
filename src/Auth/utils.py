from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from src.config import ALGORITHM, SECRET_KEY
from src.exception import ExCredentials


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_confirm_token(username: str) -> str:
    token = jwt.encode({'sub': username},
                       key=SECRET_KEY,
                       algorithm=ALGORITHM)
    return token

