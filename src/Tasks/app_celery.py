from celery import Celery

from src.config import REDIS_HOST, REDIS_PORT

celery = Celery("tasks",
                broker=f"redis://{REDIS_HOST}:{REDIS_PORT}",
                include=["src.Tasks.tasks"])
