from django.db import models


class DeliveryStatus(models.TextChoices):
    IN_PROGRESS = "in_progress", "В доставке"
    COMPLETED = "completed", "Доставлено"
