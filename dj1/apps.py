from django.apps import AppConfig


class Dj1Config(AppConfig):
    name = 'dj1'
    def ready(self):
        import users.signals
