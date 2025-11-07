from django.db import models

from butler_core.apps.mailing.enums import SendingStatus
from butler_core.apps.users.models import BotUser


class MailingSubscription(models.Model):
    user = models.ForeignKey(BotUser, verbose_name="Пользователь", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Активна", default=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {'Активна' if self.is_active else 'Неактивна'}"

    class Meta:
        verbose_name = "Подписка на рассылку"
        verbose_name_plural = "Подписки на рассылку"


class MailingLog(models.Model):
    mailing = models.ForeignKey(MailingSubscription, verbose_name="Рассылка", on_delete=models.CASCADE, null=True,
                                blank=True)
    user = models.ForeignKey(BotUser, verbose_name="Пользователь", on_delete=models.CASCADE)
    error = models.TextField(verbose_name="Ошибка", null=True, blank=True)
    sending_status = models.CharField(verbose_name="Статус отправки", max_length=255, choices=SendingStatus.choices)

    def __str__(self):
        return f"{self.user} - {self.sending_status}"

    class Meta:
        verbose_name = "Лог рассылки"
        verbose_name_plural = "Логи рассылки"
