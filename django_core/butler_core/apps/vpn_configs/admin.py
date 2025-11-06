from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from loguru import logger

from butler_core.apps.periodic_tasks.tasks import parse_configs, check_unchecked_configs
from butler_core.apps.vpn_configs.models import VpnConfig


@admin.register(VpnConfig)
class VpnConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "is_working", "is_checked")
    search_fields = ("name", "country", "is_working", "is_checked")
    list_filter = ("is_working", "is_checked")

    def get_urls(self):
        urls = super().get_urls()

        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name

        search_url = path(
            'search-configs/',
            self.admin_site.admin_view(self.process_search_configs),
            name=f'{app_label}_{model_name}_search_configs',
        )

        check_url = path(
            'check-configs/',
            self.admin_site.admin_view(self.process_check_configs),
            name=f'{app_label}_{model_name}_check_configs',
        )

        custom_urls = [search_url, check_url]
        return custom_urls + urls

    def process_search_configs(self, request):
        parse_configs.delay()
        logger.info("Запущен процесс поиска конфигов из админки")
        self.message_user(request, "Процесс поиска конфигов успешно запущен.", messages.SUCCESS)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def process_check_configs(self, request):
        check_unchecked_configs.delay()
        logger.info("Запущен процесс проверки конфигов из админки")
        self.message_user(request, "Процесс проверки конфигов успешно запущен.", messages.SUCCESS)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
