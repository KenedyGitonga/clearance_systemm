from django.apps import AppConfig


class ClearanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clearancee'

    def ready(self):
        import clearancee.signals
