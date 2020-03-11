import os

from celery import Celery
from kombu import Queue

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "get_exchange_info": {"task": "scan.tasks.get_exchange_info", "schedule": 60}
}

# https://docs.celeryproject.org/en/latest/userguide/routing.html
app.conf.task_default_queue = "celery"
app.conf.task_queues = (Queue("celery"),)
