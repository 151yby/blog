# blog_django/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_django.settings')

app = Celery('blog_django')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()