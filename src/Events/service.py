from datetime import date
from typing import List, Optional, Any
from .models import Event, Category
from src.database import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select
from src.Auth.router import current_user
from sqlalchemy import insert, values, select
from sqlalchemy.orm import selectinload


class EventManager:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_events(self) -> Any:
        """Получение всех событий"""
        query = select(Event)\
            .order_by(Event.time_event)\
            .options(selectinload(Event.category))\
            .options(selectinload(Event.organizer))\
            .options(selectinload(Event.tags))
        result = await self.session.execute(query)
        events = result.scalars().all()
        print(events)
        return events

    async def create_event(self, event, user):
        """Добавление своего события"""
        async with self.session as session:
            query = session.select(Category).where(name_category=event.category.name_category)
            result = await self.session.execute(query)
            category = result.scalars().first()

            new_event = Event(name_event=event.name_event,
                          category=category,
                          #tags=event.tags,
                          time_event=event.time_event,
                          place_event=event.place_event,
                          about_event=event.about_event,
                          price=event.price,
                          age_limit=event.age_limit,
                          image=event.image,
                          link=event.link,
                          id_organizer=user.id
                          )
            print (new_event.category)
            session.add(new_event)
            await session.commit()

    def get_event(id_event: int):
        """Получение события по id"""
        pass

    def put_event(id_event: int): #параметры
        pass

    def del_event(id_event: int):
        pass

    def get_events_search_by_name(name_event: str = ''):
        pass

    def get_categories():
        pass

    async def add_category(self, name_category):
        query = insert(Category).values(name_category=name_category)
        new_category = await self.session.execute(query)
        await self.session.commit()
        return new_category

    def get_events_category(id_category: int):
        pass

    def get_tags():
        pass

    def get_events_tag(id_tag: int):
        pass

    def get_events_on_date(current_date: date):
        pass

    def get_events_selected_user(id_user: int):
        pass

