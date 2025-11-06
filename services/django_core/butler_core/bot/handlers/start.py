from telebot import TeleBot
from telebot.types import CallbackQuery, Message
from butler_core.bot.cache.manager import RedisCacheManager
from butler_core.bot.utils import messages
from butler_core.bot.utils.error_handler import ErrorHandler
from butler_core.bot.utils.keyboards import KeyboardConstructor

from butler_core.apps.users.models import BotUser


@ErrorHandler.create()
def start(message: Message, bot: TeleBot):
    """Обработка команды '/start'."""
    telegram_id = message.chat.id
    RedisCacheManager.delete(key=telegram_id)
    username = message.from_user.first_name if message.from_user.first_name else message.from_user.username
    user, _ = BotUser.objects.update_or_create(telegram_id=telegram_id, defaults={'username': username})
    return bot.send_message(
        chat_id=telegram_id,
        text=messages.START_BOT,
    )
