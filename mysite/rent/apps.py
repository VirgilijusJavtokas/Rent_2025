from django.apps import AppConfig



class RentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rent'

    def ready(self):
        from .signals import create_profile, save_profile