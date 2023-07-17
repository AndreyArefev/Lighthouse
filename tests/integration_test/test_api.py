import pytest
from httpx import AsyncClient
from tests.conftest import open_mock_json

register_users = open_mock_json('test_register_user')
login_users = open_mock_json('test_login_user')


@pytest.mark.parametrize("user, status_code",
                         [
                             (register_users[0], 200),
                             (register_users[1], 409),
                             (register_users[2], 422),
                         ])
async def test_auth_register_user(ac: AsyncClient, user, status_code):
    response = await ac.post('/auth/register', json=user)
    assert response.status_code == status_code


@pytest.mark.parametrize("user, status_code",
                         [
                             (login_users[0], 200),
                             (login_users[1], 401),
                             (login_users[2], 401),
                         ])
async def test_auth_login_user(ac: AsyncClient, user, status_code):
    response = await ac.post('/auth/login', json=user)
    assert response.status_code == status_code
