from django.db import models
from django.contrib.auth.models import User
from .validators import validate_level
from .tasks import send_invitation_emails


NEW_STATUS = "new"
IN_PROGRESS_STATUS = "in_progress"
DONE_STATUS = "done"


class Status(models.Model):
    name = models.CharField(max_length=30, verbose_name="Name")
    key = models.CharField(max_length=30)

    def __str__(self):
        return self.name


def get_default_status():
    return Status.objects.get(key=NEW_STATUS).pk


class Task(models.Model):
    """
    Main model, based on task
    """

    title = models.CharField(max_length=50, verbose_name="Title")
    description = models.TextField(verbose_name="Task message", blank=True, null=True)

    create_date = models.DateTimeField(verbose_name="Created", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="Updated", auto_now=True)

    creator = models.ForeignKey(
        User, related_name="created", on_delete=models.CASCADE
    )
    assignees = models.ManyToManyField(
        User, verbose_name="Assignee names", blank=True
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        blank=True,
        default=get_default_status,
        null=True,
    )

    def __str__(self):
        return self.title

    def send_invites(self):
        """
        Send invitations for all user connected to task
        :param instance:
        :param assignees:
        :param is_create:
        :return:
        """
        emails = [self.creator.email]
        if self.assignees:
            assignee = self.assignees.all().values("email")
            emails.extend([email["email"] for email in assignee if email["email"]])
        send_invitation_emails.delay(emails, self.title)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
        self.send_invites()


class Image(models.Model):
    """
    Model that helps to save several images in task
    """
    image = models.ImageField(upload_to="tasks")
    task = models.ForeignKey(Task, related_name="image", on_delete=models.CASCADE)


class Comment(models.Model):
    """
    Comments in task, allow to have nested comments ( max level - 3)
    """
    text = models.TextField()
    level = models.PositiveSmallIntegerField(default=0, validators=[validate_level(2)])

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="children"
    )
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, blank=True, null=True
    )
