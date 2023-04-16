from fastapi_users import FastAPIUsers
from src.Auth.usermanager import get_user_manager
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from src.Auth.models import User
from ..config import PRIVATE_KEY


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=PRIVATE_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
