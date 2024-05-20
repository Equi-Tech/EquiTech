# Generated by Django 5.0.6 on 2024-05-20 00:27

import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_balance',
            field=models.DecimalField(decimal_places=2, default=10000.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=7, max_length=25, prefix='EQT', unique=True),
        ),
    ]
