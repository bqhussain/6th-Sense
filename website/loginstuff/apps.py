from django.apps import AppConfig
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True


class LoginstuffConfig(AppConfig):
    name = 'loginstuff'

