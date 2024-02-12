from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from bot import views as user_view


urlpatterns = [

    path('', user_view.ChatterBotAppView.as_view(), name='main'),
    path('api/chatterbot/', user_view.ChatterBotApiView.as_view(), name='chatterbot'),
]
