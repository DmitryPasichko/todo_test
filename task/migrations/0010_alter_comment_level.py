# Generated by Django 4.1.7 on 2023-02-18 09:57

from django.db import migrations, models
import task.validators


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0009_alter_comment_level"),
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
