from django.contrib import admin
from .models import Therapist,Appointment, Therapist_Registerations
# Register your models here.

admin.site.register(Therapist)
admin.site.register(Appointment)
admin.site.register(Therapist_Registerations)

