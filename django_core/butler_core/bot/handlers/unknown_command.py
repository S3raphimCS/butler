from telebot import TeleBot
from telebot.types import Message

from butler_core.apps.users.models import BotUser
from butler_core.bot.cache.manager import RedisCacheManager
from butler_core.bot.handlers.helpers import get_start_data
from butler_core.bot.utils import messages
from butler_core.bot.utils.error_handler import ErrorHandler
from butler_core.bot.utils.keyboards import KeyboardConstructor


@ErrorHandler.create()
def unknown_command(message: Message, bot: TeleBot) -> None:
    telegram_id = message.chat.id
    message_text = messages.UNKNOWN_COMMAND
    buttons = {
        "В меню": "menu"
    }
    keyboard = KeyboardConstructor(row_width=1).create_inline_keyboard(data=buttons)
    bot.send_message(telegram_id, message_text, reply_markup=keyboard)
