from django.db import models
from phone_field import PhoneField
from home.models import Profile
from django.contrib.auth.models import User
import datetime


# Create your models here.


class Therapist(models.Model):
    pdetails = models.OneToOneField(Profile, on_delete=models.CASCADE)
    credentials = models.CharField(max_length=50)
    contactNo = PhoneField(blank=True, help_text='Contact phone number')
    contactNoSecond = PhoneField(blank=True, help_text='Contact phone number second')
    fellowship = models.CharField(max_length=30)
    yearsOfExperience = models.IntegerField()

    def __str__(self):
        return self.pdetails.user.first_name


class Appointment(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointmenttime = models.DateTimeField()
    datecreated = models.DateTimeField(default=datetime.datetime.now)
    approved = models.CharField(default=1, max_length=1)
    payed = models.BooleanField(default=False)
    valid_till = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f'{self.therapist.pdetails.user.first_name} Appointment Request'




class AllAppointments(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointmenttime = models.DateTimeField()
    datecreated = models.DateTimeField(default=datetime.datetime.now)
    approved = models.CharField(default=1, max_length=1)
    payed = models.BooleanField(default=False)
    valid_till = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f'{self.therapist.pdetails.user.first_name} Appointment Record'


class Therapist_Registerations(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient.first_name} Registered with {self.therapist.pdetails.user.first_name}'

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=120)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE,default=1)
    amount = models.DecimalField(max_digits=60, decimal_places=2)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.appointment_id

class Session_Rating(models.Model):
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE,default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1)