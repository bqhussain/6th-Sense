from django.contrib import admin
from .models import Profile, Questions, Answers
# from django.contrib.auth import  get_user_model
#
# User = get_user_model()
#
# # Register your models here.
# admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Questions)
admin.site.register(Answers)
# admin.site.register(Appointment)
admin.site.site_header = 'Sixth Sense Admin Dashboard'
