from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import mapped_column, registry, relationship, Mapped
from datetime import datetime

from src.database import Base

class Category(Base):
    __tablename__ = 'categories'
    id_category: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_category: Mapped[str] = mapped_column(nullable=False, unique=True)
    events = relationship('Event', back_populates='category')

    def __str__(self):
        return self.name_category

class Event(Base):
    __tablename__ = 'events'
    id_event: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_event: Mapped[str] = mapped_column(String(200), nullable=False)
    id_category: Mapped[int] = mapped_column(ForeignKey('categories.id_category'))
    category = relationship('Category', back_populates='events')
    tags = relationship('Tag', secondary='tableEventTag', back_populates='events', passive_deletes=True)
    time_event: Mapped[datetime]
    place_event: Mapped[str]
    about_event: Mapped[str]
    price: Mapped[int]
    age_limit: Mapped[int] = mapped_column(nullable=True)
    image: Mapped[str] = mapped_column(nullable=True)
    link: Mapped[str] = mapped_column(nullable=True)
    id_organizer: Mapped[int] = mapped_column(ForeignKey('users.id'))
    organizer = relationship('User', back_populates='events')

    def __str__(self):
        return self.name_event


class Tag(Base):
    __tablename__ = 'tags'
    id_tag: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_tag: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    events = relationship('Event', secondary='tableEventTag', back_populates='tags')
    
    def __str__(self):
        return self.name_tag


tableEventTag = Table('tableEventTag',
                      Base.metadata,
                      Column('event', ForeignKey('events.id_event'), primary_key=True),
                      Column('tag', ForeignKey('tags.id_tag'), primary_key=True),
                      )
