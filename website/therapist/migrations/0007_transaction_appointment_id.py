# Generated by Django 2.1.2 on 2019-04-12 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('therapist', '0006_auto_20190412_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='appointment_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='therapist.Appointment'),
        ),
    ]
