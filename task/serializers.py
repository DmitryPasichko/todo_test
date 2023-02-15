######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import Task, Comment, Image


class ParentCommentSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        serializer_data = CommentSerializer(value).data
        return serializer_data

    class Meta:
        model = Comment
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    parent_comment = ParentCommentSerializer(
        source="children", many=True, required=False
    )
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        parent_comment = validated_data.get("parent_comment")
        level = parent_comment.level + 1 if parent_comment else 0
        validated_data["level"] = level
        instance = super().create(validated_data)
        return instance


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image", "task"]


class TaskSerializer(serializers.ModelSerializer):
    images = ImageSerializer(source="image", many=True, required=False)
    comments = CommentSerializer(
        source="comment_set",
        many=True,
        required=False,
    )

    class Meta:
        model = Task
        fields = "__all__"

    def validate_status(self, status):
        """
        Check that received status is accepted. Assigned user can not move to new and done stage
        Admin and creator - can move to any status
        :param status:
        :return:
        """
        if (
            status.key in ["new", "done"]
            and self.instance
            and self.context["request"].user in self.instance.assignees.all()
        ):
            raise ValidationError("Permission denied, you can't change status")

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance
