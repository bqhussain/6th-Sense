from django.contrib import admin
from django.urls import path, include
from . import views as botviews



urlpatterns = [

    path('webhook/', botviews.webhook),
    # path('', botviews.index),
    path('send_message/', botviews.send_message,name='saveMessage'),
    path('getMessages/', botviews.getMessages, name='getMessages'),
    path('getEvents/',botviews.eventgetter,name='getEvents')



]

