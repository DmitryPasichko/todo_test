from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Task, Comment, Image
from django.contrib.auth.models import User
from .tasks import send_invitation_emails
from rest_framework import serializers
from django.core.exceptions import ValidationError


class TaskSerializer(ModelSerializer):
    images = SerializerMethodField()
    comments = SerializerMethodField()

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

    def get_comments(self, obj):
        comments = obj.comments.all()
        result = []
        for comment in comments:
            child_level_1 = []
            for c1 in comment.children.all():
                child_level_2 = []
                for c2 in c1.children.all():
                    child_level_2.append(
                        {
                            "text": c2.text,
                            "creator_name": c2.creator.username,
                        }
                    )
                child_level_1.append(
                    {
                        "text": c1.text,
                        "creator_name": c1.creator.username,
                        "comments": child_level_2,
                    }
                )
            result.append(
                {
                    "text": comment.text,
                    "creator_name": comment.creator.username,
                    "comments": child_level_1,
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


class CommentSerializer(ModelSerializer):
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
