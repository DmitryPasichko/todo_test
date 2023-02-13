from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from .permissions import OwnDocumentPermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework import mixins
import django_filters
from .filters import TaskFilter


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
        if self.request.FILES and "images" in self.request.FILES:
            context.update({"images": self.request.FILES.getlist("images")})
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
        task = self.get_object()
        user_id = request.user.pk
        text = request.data.get("comment")
        data = {
            "text": text,
            "level": 0,
            "task": task.pk,
            "creator": user_id,
        }
        serializer = CommentSerializer(data=data)
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
