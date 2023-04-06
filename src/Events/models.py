from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Event (Base):
    __tablename__ = 'events'
    id_event = Column(Integer, primary_key=True)
    name_event = Column(String(200), nullable=False)
    id_category = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='events')
    tags = relationship('Tag', secondary='tableEventTag', back_populates='events')
    time_event = Column(TIMESTAMP)
    place_event = Column(String)
    about_event = Column(Text)
    price = Column(Integer)
    age_limit = Column(Integer)
    image = Column(String)
    link = Column(String)
    organizer = Column(String) #связать с польхователем


class Category(Base):
    __tablename__ = 'categories'
    id_category = Column(Integer, primary_key=True)
    name_category = Column(String, nullable=False)
    events = relationship('Event', back_populates='category')


class Tag(Base):
    __tablename__ = 'tags'
    id_tag = Column(Integer, primary_key=True)
    name_tag = Column(String(150), nullable=False)
    events = relationship('Event', secondary='tableEventTag', back_populates='tags')


tableEventTag = Table('table_event_tag',
                      Base.metadata,
                      Column('event', ForeignKey('events.id_event'), primary_key=True),
                      Column('tag', ForeignKey('tags.id_tag'), primary_key=True),
                      )
