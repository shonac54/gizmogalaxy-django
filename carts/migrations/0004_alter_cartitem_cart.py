# Generated by Django 5.0.1 on 2024-01-27 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_remove_cartitem_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='carts.cart'),
        ),
    ]
