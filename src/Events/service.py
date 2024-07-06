from datetime import date
#from fastapi_cache import FastAPICache
#from fastapi_cache.decorator import cache
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload, subqueryload

from src.Auth.models import User
from src.database import async_session_maker

from .models import Category, Event, Tag
from .schemas import EventCreate, CategoryCreate, Category as SCategory, CategoryWithEvent
from typing import List, Optional

class EventManager:
    """Класс отвечающий за работу с событиями"""

    @classmethod
    #@cache(expire=20)
    async def get_events(cls) -> List[Event]:
        """Получение всех событий"""
        async with async_session_maker() as session:
            query = select(Event)\
                .order_by(Event.time_event)\
                .options(selectinload(Event.category))\
                .options(selectinload(Event.organizer))\
                .options(selectinload(Event.tags))
            result = await session.execute(query)
            events = result.scalars().all()
            for e in events:
                print(e.id_event)
            return events

    @classmethod
    async def get_categories_with_events(cls) -> List[CategoryWithEvent]:
        """Получение всех категорий и связанных объектов"""
        async with async_session_maker() as session:
            query = select(Category)\
                .options(selectinload(Category.events)
                .options(subqueryload(Event.tags),subqueryload(Event.organizer)))
            result = await session.execute(query)
            events = result.scalars().all()
            print(events)
            return events

    @classmethod
    async def get_user_events(cls,
                              user_id: int) -> List[Event]:
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
            category = await cls._get_category_event(session, event.name_category)
            if event.tags:
                tags = await cls._get_list_tags_for_event(session, event.tags)
            else:
                tags = []
            print(tags)
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
            print(new_event)
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
            event = await cls._get_event_for_update(session, id_event, user)
            new_event_info.category = await cls._get_category_event(session, new_event_info.category.name_category)
            if new_event_info.tags:
                new_event_info.tags = await cls._get_list_tags_for_event(session, new_event_info.tags)
            else:
                tags = None
            if event:
                for field, value in new_event_info:
                    setattr(event, field, value)
                session.add(event)
                await session.commit()
                return event
            else:
                return None

    @classmethod
    async def del_event(cls, id_event: int) -> None:
        """Удаление события по идентификатору"""
        async with async_session_maker() as session:
            event = await session.get(Event, id_event)
            if event:
                await session.delete(event)
                await session.commit()

            else:
                raise Exception("Событие не найдено")
        async with async_session_maker() as session:
            event2 = await session.get(Event, id_event)
            print(f'Ошибка {event2}')

    @classmethod
    def get_events_search_by_name(cls, name_event: str = ''):
        pass

    @classmethod
    def get_categories(cls):
        pass

    @classmethod
    async def add_category(cls, name_category: str) -> Category:
        async with async_session_maker() as session:
            new_category = Category(name_category=name_category)
            session.add(new_category)
            await session.commit()
            return new_category

    @classmethod
    async def get_events_category(cls, id_category: int):
        async with async_session_maker() as session:
            query = session.select(Category).where(id_category=id_category)
            result = await session.execute(query)
            category = result.scalars().first()
            return category

    @classmethod
    async def _get_category_event(cls, session, name_category: str):
        query = select(Category).where(Category.name_category == name_category)
        result = await session.execute(query)
        category = result.scalars().first()
        print (category)
        return category

    @classmethod
    async def _get_list_tags_for_event(cls, session, tags):
        list_tag = []
        for tag in tags:
            query = select(Tag).where(Tag.name_tag == tag.name_tag)
            result = await session.execute(query)
            new_tag = result.scalars().first()
            if not new_tag:
                new_tag = await cls._create_tag(tag, session)
            list_tag.append(new_tag)
            print(list_tag)
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

    @staticmethod
    async def _create_tag(tag: Tag, session: AsyncSession):
        print(tag)
        print(tag.name_tag)
        new_tag = Tag(name_tag=tag.name_tag)
        print(type(new_tag))
        session.add(new_tag)
        print('OK')
        await session.flush()
        query = select(Tag).where(Tag.name_tag == tag.name_tag)
        result = await session.execute(query)
        new_tag = result.scalars().first()
        print(new_tag)
        print('OK2')
        return new_tag
        

    @classmethod
    async def _get_event_for_update(cls, session, id_event: int, user: User):
        """Получение события по id"""
        query = select(Event)\
            .where(Event.id_event == id_event and Event.id_organizer == user.id) \
            .order_by(Event.time_event)\
            .options(selectinload(Event.category))\
            .options(selectinload(Event.organizer))\
            .options(selectinload(Event.tags))
        result = await session.execute(query)
        event = result.scalars().first()
        return event if event else None
    
