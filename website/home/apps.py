from django.apps import AppConfig


class MusicsConfig(AppConfig):
    name = 'home'


    def ready(self):
        print("at ready")
        import home.signals
