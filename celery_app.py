import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

REDIS_URI = os.getenv('REDIS_URI')
app = Celery('tasks', broker=REDIS_URI)

# Настройка расписания
app.conf.beat_schedule = {
    'update_news': {
        'task': 'tasks.update_news',  
        'schedule': 900,  # Каждые 15 минут
    },
}

from tasks import update_news

