from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Task, Comment, Image
from rest_framework import serializers
from django.core.exceptions import ValidationError


class ParentCommentSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        serializer_data = CommentSerializer(value).data
        return serializer_data

    class Meta:
        model = Comment
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    parent_comment = ParentCommentSerializer(source="children", many=True)

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        parent_comment = validated_data.get("parent_comment")
        level = parent_comment.level + 1 if parent_comment else 0
        validated_data["level"] = level
        validated_data["creator"] = self.context["request"].user
        instance = super().create(validated_data)
        return instance


class TaskSerializer(ModelSerializer):
    images = SerializerMethodField()
    comments = CommentSerializer(source='comment_set', many=True, required=False,)

    class Meta:
        model = Task
        fields = "__all__"

    def get_images(self, obj):
        images = obj.image.all()
        result = []
        for image in images:
            result.append(
                {
                    "name": image.image.name,
                    "size": image.image.size,
                    "url": image.image.url,
                }
            )
        return result

    def pin_images(self, images, task):
        """
        Add images to Task
        :param images:
        :param task:
        :return:
        """
        for image in images:
            image = Image(image=image, task=task)
            image.save()

    def validate_status(self, status):
        """
        Check that received status is accepted. Assigned user can not move to new and done stage
        Admin and creator - can move to any status
        :param status:
        :return:
        """
        if (
            status.key in ["new", "done"]
            and self.instance and self.context["request"].user in self.instance.assignees.all()
        ):
            raise ValidationError("Permission denied, you can't change status")

    def create(self, validated_data):
        instance = super().create(validated_data)
        self.pin_images(self.context.get("Images", []), instance)
        return instance

    def update(self, instance, validated_data):
        # self.check_status(instance)
        instance = super().update(instance, validated_data)
        self.pin_images(self.context.get("images", []), instance)
        return instance



