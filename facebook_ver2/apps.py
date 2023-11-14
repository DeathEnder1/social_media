from django.apps import AppConfig


class FacebookVer2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'facebook_ver2'
    
    def ready(self) -> None:
        import facebook_ver2.signals
