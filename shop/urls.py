######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from .views import *

router = DefaultRouter(
    root_renderers=[OpenAPIRenderer, SwaggerUIRenderer]
)
router.register(r"product", ProductView, basename="product")
router.register(r"order", OrderView, basename="order")


urlpatterns = [
    path("", include(router.urls)),
]
