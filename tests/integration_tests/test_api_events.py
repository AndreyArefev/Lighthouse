import pytest
from httpx import AsyncClient


async def test_test(ac_auth_client: AsyncClient):
    request = await ac_auth_client.get('events/test')
    assert request.status_code == 200
