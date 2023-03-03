######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
import django_filters
from .models import TelegramUser


class TelegramUserFilter(django_filters.FilterSet):
    """
    Filter class , helps to figure out tasks by status
    """
    class Meta:
        model = TelegramUser
        fields = ["phone", "external_id"]
