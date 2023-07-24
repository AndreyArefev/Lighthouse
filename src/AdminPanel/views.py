from sqladmin import ModelView

from src.Auth.models import User
from src.Events.models import Category, Event, Tag


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


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id_category, Category.name_category]
    name = "Категория"
    name_plural = "Категории"


class TagAdmin(ModelView, model=Tag):
    column_list = [Tag.id_tag, Tag.name_tag]
    name = "Тег"
    name_plural = "Теги"
