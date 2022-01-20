from tabnanny import verbose
from django.apps import AppConfig


class LideApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lide_api'
    verbose_name = "Lide"
