# Generated by Django 4.0.3 on 2022-05-17 03:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0002_alter_post_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
