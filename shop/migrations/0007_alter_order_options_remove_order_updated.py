# Generated by Django 4.1.7 on 2023-02-18 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_order_accepted_date_order_cancelled_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created', 'status']},
        ),
        migrations.RemoveField(
            model_name='order',
            name='updated',
        ),
    ]
