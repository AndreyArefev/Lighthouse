from datetime import date
from typing import Any
from .models import Event, Category, Tag
from src.database import get_async_session
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload


class EventManager:
    """Класс отвечающий за работу с событиями"""
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
        return events

    async def create_event(self, event, user):
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

    async def get_events_category(self, id_category: int):
        query = self.session.select(Category).where(id_category=id_category)
        result = await self.session.execute(query)
        category = result.scalars().first()

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

