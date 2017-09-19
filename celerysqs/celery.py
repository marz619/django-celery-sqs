import os
import typing

from celery import Celery

# set the default django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celerysqs.settings')

from django.conf import settings  # NOQA

app = Celery('celery-sqs')  # type: Celery

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
