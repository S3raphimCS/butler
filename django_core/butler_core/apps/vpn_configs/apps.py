from django.apps import AppConfig


class VpnConfigsConfig(AppConfig):
    verbose_name = "Конфиги OpenVPN"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'butler_core.apps.vpn_configs'
