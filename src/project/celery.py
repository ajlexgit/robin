import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
app = Celery('project', include=['project.tasks'])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

from django.conf import settings
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

