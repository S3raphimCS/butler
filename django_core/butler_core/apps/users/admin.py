from django.contrib import admin
from butler_core.apps.users.models import BotUser, BaseUser


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    pass


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    pass
