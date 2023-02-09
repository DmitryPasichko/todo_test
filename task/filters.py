import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    """
    Filter class , helps to figure out tasks by status
    """
    class Meta:
        model = Task
        fields = ["status"]
