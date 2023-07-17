import asyncio
import pytest
import json
from src.database import Base, async_session_maker, engine
from src.config import MODE
from sqlalchemy import insert
from src.Auth.models import User
from src.Events.models import Event, Tag, Category, tableEventTag
from datetime import datetime
from fastapi.testclient import TestClient
from httpx import AsyncClient
from src.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """Наполняем тест.БД тестовыми данными"""
    assert MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    users = open_mock_json('users')
    events = open_mock_json('events')
    tags = open_mock_json('tags')
    categories = open_mock_json('categories')
    reletionship_event_tag = open_mock_json('reletionship_event_tag')

    for event in events:
        event["time_event"] = datetime.strptime(event["time_event"], "%Y-%m-%d %H:%M:%S")
    for user in users:
        user["registered_at"] = datetime.strptime(user["registered_at"], "%Y-%m-%d")

    print(users)

    async with async_session_maker() as session:
        add_users = insert(User).values(users)
        add_events = insert(Event).values(events)
        add_tags = insert(Tag).values(tags)
        add_categories = insert(Category).values(categories)
        add_reletionship_event_tag = insert(tableEventTag).values(reletionship_event_tag)

        await session.execute(add_users)
        await session.execute(add_events)
        await session.execute(add_tags)
        await session.execute(add_categories)
        await session.execute(add_reletionship_event_tag)

        await session.commit()


def open_mock_json(model: str):
    with open(f'tests/mock_{model}.json', 'r', encoding='utf-8') as file:
        return json.load(file)


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
def event_loop(request):
    """Создаем eventloop, необходимый для работы с асинхронными тестами"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
