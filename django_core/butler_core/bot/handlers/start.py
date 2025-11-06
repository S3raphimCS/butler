from telebot import TeleBot
from telebot.types import Message

from butler_core.apps.users.models import BotUser
from butler_core.bot.cache.manager import RedisCacheManager
from butler_core.bot.handlers.helpers import get_start_data
from butler_core.bot.utils import messages
from butler_core.bot.utils.error_handler import ErrorHandler
from butler_core.bot.utils.keyboards import KeyboardConstructor


@ErrorHandler.create()
def start(message: Message, bot: TeleBot):
    """Обработка команды '/start'."""
    telegram_id = message.chat.id
    username = message.from_user.first_name if message.from_user.first_name else message.from_user.username
    user, _ = BotUser.objects.update_or_create(telegram_id=telegram_id, defaults={'username': username})
    data = get_start_data()
    keyboard = KeyboardConstructor().create_inline_keyboard(data)
    return bot.send_message(
        chat_id=telegram_id,
        text=messages.START_BOT,
        reply_markup=keyboard,
    )
