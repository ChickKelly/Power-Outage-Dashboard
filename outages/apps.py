from django.apps import AppConfig

class OutagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'outages'

    def ready(self):
        import sys
        if 'runserver' in sys.argv:
            from .mqtt_listener import start_mqtt
            start_mqtt()
