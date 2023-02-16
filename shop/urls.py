######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from .views import *

schema_view = get_swagger_view(title="Pastebin API")


urlpatterns = [
    path("", index),
    path("about/", about),
    path("products/", products),
    path("fashion/", fashion),
    path("news/", news),
    path("contact/", contacts),
]
