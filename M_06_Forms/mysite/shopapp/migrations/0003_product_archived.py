# Generated by Django 4.0.6 on 2022-07-24 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_product_created_at_product_discount_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
