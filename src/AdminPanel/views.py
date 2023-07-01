from sqladmin import ModelView
from src.Auth.models import User
from src.Events.models import Event, Category, Tag


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

class EventAdmin(ModelView, model=Event):
    column_list = [Event.id_event, Event.name_event]
    name = "Событие"
    name_plural = "События"

