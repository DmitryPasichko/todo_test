######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from .celery import app as celery_app

__all__ = ('celery_app', )