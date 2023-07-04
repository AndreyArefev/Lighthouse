from datetime import date
from typing import Any
from .models import Event, Category, Tag
from src.Auth.models import User
from .schemas import EventCreate
from src.database import get_async_session
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from fastapi_cache.decorator import cache


class EventManager:
    """Класс отвечающий за работу с событиями"""
    def __init__(self,
                 session: AsyncSession = Depends(get_async_session)):
        self.session = session

    @cache(expire=20)
    async def get_events(self) -> [Event]:
        """Получение всех событий"""
        async with self.session as session:
            query = select(Event)\
                .order_by(Event.time_event)\
                .options(selectinload(Event.category))\
                .options(selectinload(Event.organizer))\
                .options(selectinload(Event.tags))
            result = await session.execute(query)
            events = result.scalars().all()
            return events

    async def get_user_events(self,
                              user_id: int) -> [Event]:
        """Получение всех событий конкретного пользователя"""
        async with self.session as session:
            query = select(Event)\
                .where(Event.id_organizer == user_id)\
                .order_by(Event.time_event)\
                .options(selectinload(Event.category))\
                .options(selectinload(Event.organizer))\
                .options(selectinload(Event.tags))
            result = await session.execute(query)
            events = result.scalars().all()
            return events

    async def create_event(self,
                           event: EventCreate,
                           user: User) -> Event:
        """Добавление своего события"""
        async with self.session as session:
            category = await self._get_category(event.category.name_category)
            tags = await self.tag_get_and_create(event.tags)
            new_event = Event(name_event=event.name_event,
                              category=category,
                              tags=tags,
                              time_event=event.time_event,
                              place_event=event.place_event,
                              about_event=event.about_event,
                              price=event.price,
                              age_limit=event.age_limit,
                              image=event.image,
                              link=event.link,
                              id_organizer=user.id,
                              organizer=user,
                              )
            session.add(new_event)
            await session.commit()
            return new_event

    async def get_event(self, id_event: int) -> Event | None:
        """Получение события по id"""
        async with self.session as session:
            query = select(Event)\
                .where(Event.id_event == id_event)\
                .order_by(Event.time_event)\
                .options(selectinload(Event.category))\
                .options(selectinload(Event.organizer))\
                .options(selectinload(Event.tags))
            result = await session.execute(query)
            event = result.scalars().one_or_none()
            return event if event else None

    async def put_event(self, new_event_info: EventCreate, id_event: int, user: User) -> Event | None:
        """Изменение события по id"""
        async with self.session as session:
            event = await self._get_event_for_update(id_event, user)
            new_event_info.category = await self._get_category(new_event_info.category.name_category)
            new_event_info.tags = await self.tag_get_and_create(new_event_info.tags)
            if event:
                for field, value in new_event_info:
                    setattr(event, field, value)
                await session.commit()
                return event
            else:
                return None

    def del_event(id_event: int):
        pass

    def get_events_search_by_name(name_event: str = ''):
        pass

    def get_categories():
        pass

    async def add_category(self, name_category):
        async with self.session as session:
            query = insert(Category).values(name_category=name_category).returning(Category)
            new_category = await self.session.execute(query)
            await session.commit()
            return new_category.scalar()

    async def get_events_category(self, id_category: int):
        async with self.session as session:
            query = session.select(Category).where(id_category=id_category)
            result = await session.execute(query)
            category = result.scalars().first()
            return category

    async def _get_category(self, name_category: str):
        query = select(Category).where(Category.name_category == name_category)
        result = await self.session.execute(query)
        category = result.scalars().first()
        return category

    async def tag_get_and_create(self, tags):
        list_tag = []
        for tag in tags:
            query = select(Tag).where(Tag.name_tag == tag.name_tag)
            result = await self.session.execute(query)
            new_tag = result.scalars().first()
            if not new_tag:
                new_tag = Tag(name_tag=tag.name_tag)
                self.session.add(new_tag)
                await self.session.commit()
            list_tag.append(new_tag)
        return list_tag


    def get_events_tag(id_tag: int):
        pass

    def get_events_on_date(current_date: date):
        pass

    def get_events_selected_user(id_user: int):
        pass

    async def _get_event_for_update(self, id_event: int, user: User):
        """Получение события по id"""
        async with self.session as session:
            query = select(Event)\
                .where(Event.id_event == id_event and Event.id_organizer == user.id) \
                .order_by(Event.time_event)\
                .options(selectinload(Event.category))\
                .options(selectinload(Event.organizer))\
                .options(selectinload(Event.tags))
            result = await session.execute(query)
            event = result.scalars().first()
            return event if event else None



