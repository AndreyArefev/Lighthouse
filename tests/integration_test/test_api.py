import json
import pytest
from httpx import AsyncClient
from contextlib import nullcontext as does_not_reise
from src.exception import ExUsernameAlreadyExists
from tests.conftest import open_mock_json
from fastapi.exceptions import HTTPException

users = open_mock_json('test_register_user')

@pytest.mark.parametrize("user, status_code",
                         [
                             (users[0], 200),
                             (users[1], 409)
                         ])
async def test_auth_register_user(ac: AsyncClient, user, status_code):
    response = await ac.post('/auth/register', json=user)
    assert response.status_code == status_code
