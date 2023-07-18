from datetime import date
from typing import Any
from .models import Event, Category, Tag
from src.Auth.models import User
from .schemas import EventCreate
from src.database import async_session_maker
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from fastapi_cache.decorator import cache


class EventManager:
    """Класс отвечающий за работу с событиями"""

    @classmethod
    @cache(expire=20)
    async def get_events(cls) -> [Event]:
        """Получение всех событий"""
        async with async_session_maker() as session:
            query = select(Event)\
                .order_by(Event.time_event)\
                .options(selectinload(Event.category))\
                .options(selectinload(Event.organizer))\
                .options(selectinload(Event.tags))
            result = await session.execute(query)
            events = result.scalars().all()
            return events

    @classmethod
    async def get_user_events(cls,
                              user_id: int) -> [Event]:
        """Получение всех событий конкретного пользователя"""
        async with async_session_maker() as session:
            query = select(Event)\
                .where(Event.id_organizer == user_id)\
                .order_by(Event.time_event)\
                .options(selectinload(Event.category))\
                .options(selectinload(Event.organizer))\
                .options(selectinload(Event.tags))
            result = await session.execute(query)
            events = result.scalars().all()
            return events

    @classmethod
    async def create_event(cls,
                           event: EventCreate,
                           user: User) -> Event:
        """Добавление своего события"""
        async with async_session_maker() as session:
            category = await cls._get_category(session, event.category.name_category)
            tags = await cls.tag_get_or_create(session, event.tags)
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

    @classmethod
    async def get_event(cls, id_event: int) -> Event | None:
        """Получение события по id"""
        async with async_session_maker() as session:
            query = select(Event)\
                .where(Event.id_event == id_event)\
                .order_by(Event.time_event)\
                .options(selectinload(Event.category))\
                .options(selectinload(Event.organizer))\
                .options(selectinload(Event.tags))
            result = await session.execute(query)
            event = result.scalars().one_or_none()
            return event if event else None

    @classmethod
    async def put_event(cls, new_event_info: EventCreate, id_event: int, user: User) -> Event | None:
        """Изменение события по id"""
        async with async_session_maker() as session:
            event = await cls._get_event_for_update(id_event, user)
            new_event_info.category = await cls._get_category(session, new_event_info.category.name_category)
            new_event_info.tags = await cls.tag_get_or_create(session, new_event_info.tags)
            if event:
                for field, value in new_event_info:
                    setattr(event, field, value)
                await session.commit()
                return event
            else:
                return None

    @classmethod
    def del_event(cls, id_event: int):
        pass

    @classmethod
    def get_events_search_by_name(cls, name_event: str = ''):
        pass

    @classmethod
    def get_categories(cls):
        pass

    @classmethod
    async def add_category(cls, name_category):
        async with async_session_maker() as session:
            query = insert(Category).values(name_category=name_category).returning(Category)
            new_category = await session.execute(query)
            await session.commit()
            return new_category.scalar()

    @classmethod
    async def get_events_category(cls, id_category: int):
        async with async_session_maker() as session:
            query = session.select(Category).where(id_category=id_category)
            result = await session.execute(query)
            category = result.scalars().first()
            return category

    @classmethod
    async def _get_category(cls, session, name_category: str):
        query = select(Category).where(Category.name_category == name_category)
        result = await session.execute(query)
        category = result.scalars().first()
        return category

    @classmethod
    async def tag_get_or_create(cls, session, tags):
        list_tag = []
        for tag in tags:
            query = select(Tag).where(Tag.name_tag == tag.name_tag)
            result = await session.execute(query)
            new_tag = result.scalars().first()
            if not new_tag:
                new_tag = Tag(name_tag=tag.name_tag)
                session.add(new_tag)
                await session.flush()
            list_tag.append(new_tag)
        return list_tag

    @classmethod
    def get_events_tag(cls, id_tag: int):
        pass

    @classmethod
    def get_events_on_date(cls, current_date: date):
        pass

    @classmethod
    def get_events_selected_user(cls, id_user: int):
        pass

    @classmethod
    async def _get_event_for_update(cls, id_event: int, user: User):
        """Получение события по id"""
        async with async_session_maker() as session:
            query = select(Event)\
                .where(Event.id_event == id_event and Event.id_organizer == user.id) \
                .order_by(Event.time_event)\
                .options(selectinload(Event.category))\
                .options(selectinload(Event.organizer))\
                .options(selectinload(Event.tags))
            result = await session.execute(query)
            event = result.scalars().first()
            return event if event else None



