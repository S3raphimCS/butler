from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class Command(BaseCommand):
    """Команда для создания периодических задач."""

    help = 'Создание периодических задач'

    def handle(self, *args, **options):
        """Консольный вывод."""
        self.stdout.write("Начато создание периодических задач:\n")
        start = timezone.now()
        self._setup_tasks()
        self.stdout.write(
            "Периодические задачи созданы. Время: "
            f"{(timezone.now() - start).seconds / 60:.2f} мин"
        )

    @staticmethod
    def _setup_tasks():
        """Периодические задачи."""

        every_one_min_cron, _ = CrontabSchedule.objects.get_or_create(
            minute='*/1',
            timezone=settings.TIME_ZONE,
        )

        every_five_min_cron, _ = CrontabSchedule.objects.get_or_create(
            minute='*/5',
            timezone=settings.TIME_ZONE,
        )

        every_one_hour_cron, _ = CrontabSchedule.objects.get_or_create(
            minute='*/60',
            timezone=settings.TIME_ZONE,
        )

        every_twelve_hour_cron, _ = CrontabSchedule.objects.get_or_create(
            minute="0",
            hour="*/12",
            timezone=settings.TIME_ZONE
        )

        daily_at_12_00_cron, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='12',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
            timezone=settings.TIME_ZONE,
        )

        daily_at_08_00_cron, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='8',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
            timezone=settings.TIME_ZONE,
        )

        daily_at_02_00_cron, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='2',
            timezone=settings.TIME_ZONE,
        )

        daily_at_14_00_cron, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='14',
            timezone=settings.TIME_ZONE,
        )

        _ = PeriodicTask.objects.update_or_create(
            name='Получение новых конфигов с сайта',
            defaults={
                'crontab': daily_at_12_00_cron,
                'task': 'butler_core.apps.periodic_tasks.tasks.parse_configs',
            }
        )

        _ = PeriodicTask.objects.update_or_create(
            name="Ежедневная рассылка",
            defaults={
                'crontab': daily_at_08_00_cron,
                'task': 'butler_core.apps.periodic_tasks.tasks.send_daily_mailing'
            }
        )

        _ = PeriodicTask.objects.update_or_create(
            name="Проверка полученных конфигов на работоспособность",
            defaults={
                "crontab": daily_at_14_00_cron,
                "task": "butler_core.apps.periodic_tasks.tasks.check_unchecked_configs"
            }
        )

        _ = PeriodicTask.objects.update_or_create(
            name='Проверка уже работающих конфигов на работоспособность',
            defaults={
                'crontab': daily_at_02_00_cron,
                'task': 'butler_core.apps.periodic_tasks.tasks.recheck_working_configs',
            }
        )
