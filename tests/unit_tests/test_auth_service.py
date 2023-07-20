import pytest

from src.Auth.service import UserManager
from tests.conftest import open_mock_json

users = open_mock_json('users')


@pytest.mark.parametrize("user, my_filter",
                         [
                             (users[0], {"username": "string92"}),
                             (users[1], {"email": "user@example.com"}),
                             (None, {"email": "new_user@example.com"})
                         ])
async def test_find_user_one_or_none(user: dict | None, my_filter: dict):
    usermanager = UserManager()
    find_user = await usermanager.find_user_one_or_none(**my_filter)
    if user:
        assert find_user.id == user['id']
    else:
        assert not find_user


