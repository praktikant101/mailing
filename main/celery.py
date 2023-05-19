import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_mailing_stats': {
        'task': 'app.tasks.send_mailing_stats',
        'schedule': crontab(minute=0, hour=0),
    },
}

app.autodiscover_tasks()