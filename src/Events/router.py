import service
from typing import List
from fastapi import APIRouter, Query, Response, status
from datetime import date
from .schemas import Event, Category, Tag


router = APIRouter(
    prefix='/events',
    tags=['Events']
)


@router.get('/',
            response_model=List[Event])
def get_events():
    return service.get_events()


@router.post('/',
             response_model=Event,
             status_code=status.HTTP_201_CREATED)
def add_event(event: Event):
    return service.add_event()


@router.get('/search',
            response_model=List[Event])
def get_events_search_by_name(name_event: str = Query()):
    return service.get_events_search_by_name(name_event)


@router.get('/{id_event}',
            response_model=Event)
def get_event(id_event: int):
    return service.get_event(id_event)


@router.put('/{id_event}',
            response_model=Event)
def put_event(id_event: int):
    return service.put_event(id_event)


@router.delete('/{id_event}',
               status_code=status.HTTP_204_NO_CONTENT)
def del_event(id_event: int):
    return service.del_event(id_event)


@router.get('/categories',
            response_model=List[Category])
def get_categories():
    return service.get_categories()


@router.get('/categories/{id_category}',
            response_model=Category)
def get_events_category(id_category: int):
    return service.get_events_category(id_category)


@router.get('/tags',
            response_model=List[Tag])
def get_tags():
    return service.get_tags()


@router.get('/tags/{id_tag}',
            response_model=Tag)
def get_events_tag(id_tag: int):
    return service.get_events_tag(id_tag)


@router.get('/calendar/{current_date}',
            response_model=List[Event])
def get_events_on_date(current_date: date):
    return service.get_events_on_date(current_date)


@router.get('/{id_user}',
            response_model=List[Event])
def get_events_selected_user(id_user: int):
    return service.get_events_selected_user(id_user)
