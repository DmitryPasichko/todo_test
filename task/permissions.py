from rest_framework import permissions


class OwnDocumentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        """
        Check user permissions to Task model:
        If user is creator -allow all permissions
        if user assigned to task - can read and update
        ather user - only read
        :param request:
        :param view:
        :param obj:
        :return:
        """
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or (
                user in obj.assignee_ids.all()
                and request.method in (*permissions.SAFE_METHODS, "PATCH", "POST")
            )
            or user == obj.creator_id
        )


class OwnCommentsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        """
        It checks that all users can read Comments and create only if you are assigned or creator or admin
        :param request:
        :param view:
        :param obj:
        :return:
        """
        user = request.user
        level = obj.level
        task = (
            obj.task
            if level == 0
            else obj.parent_comment.task
            if level == 1
            else obj.parent_comment.parent_comment.task
        )
        return (
            request.method in permissions.SAFE_METHODS
            or user in task.assignee_ids.all()
            or user == obj.creator_id
            or user.is_superuser
        )
