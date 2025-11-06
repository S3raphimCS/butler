from django.db import models

from butler_core.apps.packages.enums import DeliveryStatus
from butler_core.apps.users.models import BotUser


class Package(models.Model):
    user = models.ForeignKey(BotUser, verbose_name="Пользователь", on_delete=models.CASCADE)
    track_id = models.CharField(max_length=255, verbose_name="Трек номер")
    status = models.CharField(verbose_name="Статус доставки", max_length=255, choices=DeliveryStatus.choices,
                              default=DeliveryStatus.IN_PROGRESS)
    last_info = models.TextField(verbose_name="Последняя информация",  null=True, blank=True)

    class Meta:
        verbose_name = "Посылка"
        verbose_name_plural = "Посылки"
