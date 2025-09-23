from django.apps import AppConfig

class LocalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'locales'

    def ready(self):
        import locales.signals  # ✅ Importa aquí, no arriba del archivo
