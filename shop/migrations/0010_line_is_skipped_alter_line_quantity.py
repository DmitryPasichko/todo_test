# Generated by Django 4.1.7 on 2023-02-19 09:23

from django.db import migrations, models
import shop.validators


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0009_alter_product_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="line",
            name="is_skipped",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="line",
            name="quantity",
            field=models.PositiveSmallIntegerField(
                validators=[shop.validators.validate_line_quantity]
            ),
        ),
    ]
