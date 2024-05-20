from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Query, status

from src.Auth.dependencies import get_current_active_user as current_user
from src.Auth.models import User

from .schemas import Category, Event, EventCreate, Tag
from .service import EventManager
import src.config as c

UPLOAD_FOLDER = "static/images"  # Папка для хранения изображений

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

router = APIRouter(
    prefix='/events',
    tags=['События']
)


@router.get('/test')
async def get_test(user: User = Depends(current_user)):
    return user


@router.get('/',
            response_model=List[Event])
async def get_events(user: User = Depends(current_user)):
    all_events = await EventManager.get_events()
    return all_events


@router.get('/{user_id}/',
            response_model=List[Event])
async def get_events(user_id: int,
                     user: User = Depends(current_user)):
    all_user_events = await EventManager.get_user_events(user_id)
    return all_user_events


@router.post('/',
             response_model=Event,
             status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate,
                       user: User = Depends(current_user)):
    new_event = await EventManager.create_event(event, user)
    return new_event


@router.get('/{id_event}',
            response_model=Event | str)
async def get_event(id_event: int,
                    user: User = Depends(current_user)):
    event = await EventManager.get_event(id_event)
    return event if event else 'Событие отсутствует'


@router.put('/{id_event}',
            response_model=Event | str)
async def put_event(event: EventCreate,
                    id_event: int,
                    user: User = Depends(current_user)):
    event = await EventManager.put_event(event, id_event, user)
    return event if event else 'Вы не можете изменить данное событие'


@router.delete('/{id_event}',
               status_code=status.HTTP_204_NO_CONTENT)
def del_event(id_event: int):
    return EventManager.del_event(id_event)


@router.get('/search',
            response_model=List[Event])
def get_events_search_by_name(name_event: str = Query()):
    return EventManager.get_events_search_by_name(name_event)


@router.get('/categories', response_model=List[Category])
def get_categories():
    return EventManager.get_categories()


@router.get('/categories/{id_category}',
            response_model=Category)
def get_events_category(id_category: int):
    return EventManager.get_events_category(id_category)


@router.get('/tags',
            response_model=List[Tag])
def get_tags():
    return EventManager.get_tags()


@router.get('/tags/{id_tag}',
            response_model=Tag)
def get_events_tag(id_tag: int):
    return EventManager.get_events_tag(id_tag)


@router.get('/calendar/{current_date}',
            response_model=List[Event])
def get_events_on_date(current_date: date):
    return EventManager.get_events_on_date(current_date)


@router.get('/{id_user}',
            response_model=List[Event])
def get_events_selected_user(id_user: int):
    return EventManager.get_events_selected_user(id_user)


@router.post("/upload/")
async def upload_image(file: UploadFile = File(...), request: Request):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as image_file:
        content = await file.read()
        image_file.write(content)
    base_url = request.base_url
    image_url = f"{base_url}images/{file.filename}"
    return image_url


@app.get("/images/{image_path}") 
async def get_image(image_path: str):
    if not image_рath:
        raise HTTPException(status_code=400, detail="Image URL is required")
    return FileResponse(image_path)