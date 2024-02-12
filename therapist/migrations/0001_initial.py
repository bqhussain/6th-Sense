# Generated by Django 2.1.2 on 2019-03-02 16:20

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointmenttime', models.DateTimeField()),
                ('datecreated', models.DateTimeField(default=datetime.datetime.now)),
                ('approved', models.CharField(default=1, max_length=1)),
                ('payed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Therapist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credentials', models.CharField(max_length=50)),
                ('contactNo', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
                ('contactNoSecond', phone_field.models.PhoneField(blank=True, help_text='Contact phone number second', max_length=31)),
                ('fellowship', models.CharField(max_length=30)),
                ('yearsOfExperience', models.IntegerField()),
                ('pdetails', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='therapist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='therapist.Therapist'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
