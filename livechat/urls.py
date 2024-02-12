from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    # path('home/', views.Home, name='home'),
    # path('post/', views.Post, name='post'),
    path('saveMessage/', views.saveMessage, name='saveMessage'),
    path('getMessages/', views.getMessages, name='getMessages'),
    # path('messages/', views.Messages, name='messages'),
    path('', views.ChatWindow, name='chatbox'),

    # url(r'^post/$', views.Post, name='post'),
    # url(r'^messages/$', views.Messages, name='messages'),
]
