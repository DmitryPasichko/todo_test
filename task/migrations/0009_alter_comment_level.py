# Generated by Django 4.1.7 on 2023-02-18 09:30

from django.db import migrations, models
import task.validators


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0008_alter_comment_level_alter_image_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="level",
            field=models.PositiveSmallIntegerField(
                default=0, validators=[task.validators.validate_level]
            ),
        ),
    ]
