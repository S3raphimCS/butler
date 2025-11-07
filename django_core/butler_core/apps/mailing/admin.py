from django.contrib import admin

from butler_core.apps.mailing.models import MailingLog, MailingSubscription


class MailingLogInline(admin.TabularInline):
    model = MailingLog
    extra = 0


@admin.register(MailingSubscription)
class MailingSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active", "created_at")
    search_fields = ("user_id",)
    list_filter = ("is_active", "created_at")
    inlines = [MailingLogInline]
