# Generated by Django 2.1.2 on 2019-03-06 18:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('therapist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='valid_till',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
