from django.db import models


class VpnConfig(models.Model):
    """Модель конфига VPN"""

    name = models.CharField(verbose_name="Название", max_length=255, null=True, blank=True)
    country = models.CharField(verbose_name="Страна", max_length=255, null=True, blank=True)
    is_working = models.BooleanField(verbose_name="Рабочий", default=False)
    is_checked = models.BooleanField(verbose_name="Проверен", default=False)
    file = models.FileField(verbose_name="Файл", upload_to="vpn/", null=True, blank=True)
    timestamp = models.DateTimeField(verbose_name="Дата скачивания", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "VPN-конфиг"
        verbose_name_plural = "VPN-конфиги"
