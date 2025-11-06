from django.apps import AppConfig


class PeriodicTasksConfig(AppConfig):
    verbose_name = "Периодические задачи"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'butler_core.apps.periodic_tasks'
