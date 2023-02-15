######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todo.settings")

app = Celery('send_email')
app.config_from_object("django.conf:settings", namespace='CELERY')
app.autodiscover_tasks()