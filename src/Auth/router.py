from fastapi_users import FastAPIUsers
from src.Auth.models import User
from src.Auth.usermanager import get_user_manager
from src.Auth.service import auth_backend


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

