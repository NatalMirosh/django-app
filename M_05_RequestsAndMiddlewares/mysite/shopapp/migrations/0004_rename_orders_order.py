# Generated by Django 4.2 on 2023-05-11 11:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogapp', '0003_orders_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Orders',
            new_name='Order',
        ),
    ]
