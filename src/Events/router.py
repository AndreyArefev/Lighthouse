from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Query, status
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import FileResponse

from src.Auth.dependencies import get_current_active_user as current_user, get_current_superuser
from src.Auth.models import User
from src.Events.utils import get_unique_filename

from .schemas import Category, Event, EventCreate, Tag, CategoryCreate, WrapperCategoryCreate, CategoryWithEvent
from .service import EventManager
import src.config as c
import os

UPLOAD_FOLDER = "static/images"  # Папка для хранения изображений

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

router = APIRouter(
    prefix='/events',
    tags=['События']
)

@router.get('/test_without_auth')
async def get_test():
    return True

@router.get('/test_with_auth')
async def get_test(user: User = Depends(current_user)):
    return user


@router.get('/',
            response_model=List[Event])
async def get_events():
    all_events = await EventManager.get_events()
    return all_events

@router.get('/categories', 
            response_model=WrapperCategoryCreate)
async def get_categories_with_events():
    all_categories_with_events = await EventManager.get_categories_with_events()
    return {'all_events': all_categories_with_events}


@router.get('/{user_id}/',
            response_model=List[Event])
async def get_events_current_user(user_id: int,
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
               status_code=status.HTTP_204_NO_CONTENT) #права админа
async def del_event(id_event: int):
    await EventManager.del_event(id_event)



@router.get('/search',
            response_model=List[Event])
def get_events_search_by_name(name_event: str = Query()):
    return EventManager.get_events_search_by_name(name_event)


@router.get('/categories_list', response_model=List[Category])
def get_categories():
    return EventManager.get_categories()

@router.post('/add_category', 
             response_model=Category,
             status_code=status.HTTP_201_CREATED)
async def add_category(category: CategoryCreate,
                       user: User = Depends(current_user)): #установить только админский доступ
    new_category = await EventManager.add_category(category.name_category)
    return new_category


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

UPLOAD_FOLDER = "static/images"  # Папка для хранения изображений
@router.post("/upload/")
async def upload_image(request: Request, file: UploadFile = File(...)):
    '''Загрузка файлов на сервер'''
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    while os.path.exists(file_path):
        file.filename = get_unique_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        with open(file_path, "wb") as image_file:
            content = await file.read()
            image_file.write(content)
    except IOError as e:
        raise HTTPException(status_code=500, detail="Error saving the file")
    base_url = request.base_url
    image_url = f"{base_url}events/get_image/{file.filename}"
    return image_url


@router.get("/get_image/{image_name}") 
async def get_image(image_name: str):
    image_path = os.path.join(UPLOAD_FOLDER, image_name)
    return FileResponse(image_path)