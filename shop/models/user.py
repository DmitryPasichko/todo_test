######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from django.db import models
from django.contrib.auth.models import User


class TelegramUser(User):

    phone = models.CharField(max_length=13)
    external_id = models.CharField(max_length=100)
    country = models.CharField(max_length=50, default="Ukraine", blank=True)
    language = models.CharField(max_length=30, default="en", blank=True)
    balance = models.CharField(max_length=30, default= 'USD', blank=True)
