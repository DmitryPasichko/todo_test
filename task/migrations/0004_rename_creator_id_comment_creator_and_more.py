# Generated by Django 4.1.6 on 2023-02-13 09:51

from django.db import migrations, models
import task.validators


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0003_alter_comment_level_alter_image_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="creator_id",
            new_name="creator",
        ),
        migrations.RenameField(
            model_name="image",
            old_name="task_id",
            new_name="task",
        ),
        migrations.RenameField(
            model_name="task",
            old_name="assignee_ids",
            new_name="assignees",
        ),
        migrations.RenameField(
            model_name="task",
            old_name="creator_id",
            new_name="creator",
        ),
        migrations.AlterField(
            model_name="comment",
            name="level",
            field=models.PositiveSmallIntegerField(
                default=0, validators=[task.validators.validate_level]
            ),
        ),
    ]
