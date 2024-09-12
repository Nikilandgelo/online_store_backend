import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graduate_work.settings')

app = Celery('graduate_work')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

__all__ = ('app',)
