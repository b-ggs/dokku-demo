import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dokku_demo.settings.base")

app = Celery("dokku_demo")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
