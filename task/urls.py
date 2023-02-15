######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import TaskViewSet, CommentViewSet


router = DefaultRouter(
    root_renderers=[OpenAPIRenderer, SwaggerUIRenderer]
)
# router = SimpleRouter()
router.register(r"task", TaskViewSet, basename="task")
router.register(r"comment", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
