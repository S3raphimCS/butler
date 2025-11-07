from django.apps import AppConfig


class MailingConfig(AppConfig):
    verbose_name = 'Рассылки'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'butler_core.apps.mailing'
