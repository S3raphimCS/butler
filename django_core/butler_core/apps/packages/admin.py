from django.contrib import admin

from butler_core.apps.packages.models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    pass
