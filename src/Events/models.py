from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from src.database import Base


class Event(Base):
    __tablename__ = 'event'
    id_event = Column(Integer, primary_key=True)
    name_event = Column(String(200), nullable=False)
    id_category = Column(Integer, ForeignKey('category.id_category'))
    category = relationship('Category', back_populates='events')
    tags = relationship('Tag', secondary='tableEventTag', back_populates='events')
    time_event = Column(TIMESTAMP)
    place_event = Column(String)
    about_event = Column(Text)
    price = Column(Integer)
    age_limit = Column(Integer)
    image = Column(String)
    link = Column(String)
    id_organizer = Column(Integer, ForeignKey('user.id'))
    organizer = relationship('User', back_populates='events')


class Category(Base):
    __tablename__ = 'category'
    id_category = Column(Integer, primary_key=True)
    name_category = Column(String, nullable=False, unique=True)
    events = relationship('Event', back_populates='category')


class Tag(Base):
    __tablename__ = 'tag'
    id_tag = Column(Integer, primary_key=True)
    name_tag = Column(String(150), nullable=False, unique=True)
    events = relationship('Event', secondary='tableEventTag', back_populates='tags')


tableEventTag = Table('tableEventTag',
                      Base.metadata,
                      Column('event', ForeignKey('event.id_event'), primary_key=True),
                      Column('tag', ForeignKey('tag.id_tag'), primary_key=True),
                      )
