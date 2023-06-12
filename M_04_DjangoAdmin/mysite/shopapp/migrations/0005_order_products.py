# Generated by Django 4.2 on 2023-05-11 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0004_rename_orders_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', to='blogapp.product'),
        ),
    ]
