from django.core.management import BaseCommand
from loguru import logger
from telebot import util

from butler_core.bot.main import bot


class Command(BaseCommand):
    """Команда для запуска пулинга телеграм бота."""

    help = 'Запуск телеграм бота'

    def handle(self, *args, **options):
        try:
            logger.info('Бот запущен')
            bot.infinity_polling(allowed_updates=util.update_types, timeout=60)
        except KeyboardInterrupt:
            logger.error('Бот остановлен')
        except Exception as exc:
            logger.error('Ошибка запуска бота: {exc}'.format(exc=exc))
