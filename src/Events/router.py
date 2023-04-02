from fastapi import FastAPI, APIRouter, Query

router = APIRouter()


@router.get('/')
def get_home_page():
    return 'home_page'


@router.get('/events')
def get_events():
    return 'какую-то логику'


@router.get('/events/search')
def get_events_search_by_name(name_event: str = Query()):
    return 'какую-то логику'


@router.get('/events/{id_event}')
def get_event(id_event: int):
    return 'какую-то логику'


@router.get('/events/categories')
def get_categories():
    return 'какую-то логику'


@router.get('/events/categories/{id_category}')
def get_events_category(id_category: int):
    return 'какую-то логику'


@router.get('/events/tags')
def get_tags():
    return 'какую-то логику'


@router.get('/events/tags/{id_tag}')
def get_events_tag(id_tag: int):
    return 'какую-то логику'


@router.get('/events/calendar/{date}')
def get_events_on_date(date: date):
    return 'какую-то логику'


@router.get('/events/{id_user}')
def get_events_selected_user(id_user: int):
    return 'какую-то логику'