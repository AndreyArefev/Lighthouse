import asyncio
import pytest
import json
from src.database import Base, async_session_maker, engine
from src.config import MODE
from sqlalchemy import insert
from src.Auth.models import User
from src.Events.models import Event, Tag, Category


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """Наполняем тест.БД тестовыми данными"""
    assert MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'src/tests/mock_{model}.json', 'r') as file:
            return json.load(file)

    users = open_mock_json('users')
    events = open_mock_json('events')
    tags = open_mock_json('tags')
    categories = open_mock_json('categories')

    async with async_session_maker() as session:
        add_users = insert(User).values(users)
        add_events = insert(Event).values(events)
        add_tags = insert(Tag).values(tags)
        add_categories = insert(Category).values(categories)

        await session.execute(add_users)
        await session.execute(add_events)
        await session.execute(add_tags)
        await session.execute(add_categories)

        await session.commit()

@pytest.fixture(scope='session')
def event_loop(request):
    """Создаем eventloop, необходимый для работы с асинхронными тестами"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()