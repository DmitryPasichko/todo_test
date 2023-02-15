from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

import django_filters

from .filters import TaskFilter
from .models import Task, Comment
from .permissions import OwnDocumentPermission
from .serializers import TaskSerializer, CommentSerializer, ImageSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = (
        OwnDocumentPermission,
        IsAuthenticated,
    )
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if "assignees" in self.request.POST:
            context.update({"assignees": self.request.POST.get("assignees", [])})
        return context

    @action(
        detail=True,
        methods=["post"],
        permission_classes=(
            OwnDocumentPermission,
            IsAuthenticated,
        ),
    )
    def comment(self, request, pk=None):
        """
        Add new comment to task
        :param request:
        :param pk:
        :return:
        """
        serializer = CommentSerializer(
            data={**request.data, "task": pk}, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=request.user)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=(
            OwnDocumentPermission,
            IsAuthenticated,
        ),
    )
    def image(self, request, pk=None):
        """
        Add new image to task
        :param request:
        :param pk:
        :return:
        """
        data = {
            "image": request.FILES.get("image"),
            "task": pk,
        }
        serializer = ImageSerializer(data=data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CommentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)
