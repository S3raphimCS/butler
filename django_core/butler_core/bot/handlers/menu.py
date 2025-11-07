from telebot import TeleBot
from telebot.types import CallbackQuery, Message

from butler_core.bot.handlers.helpers import get_menu_data
from butler_core.bot.utils import messages
from butler_core.bot.utils.error_handler import ErrorHandler
from butler_core.bot.utils.keyboards import KeyboardConstructor


@ErrorHandler.create()
def menu(message: Message, bot: TeleBot):
    """Обработка колбека на получение меню"""

    telegram_id = message.chat.id
    message = messages.MENU_TEXT
    data = get_menu_data()
    keyboard = KeyboardConstructor().create_inline_keyboard(data)

    return bot.send_message(telegram_id, message, reply_markup=keyboard)


@ErrorHandler.create()
def menu_callback(callback: CallbackQuery, bot: TeleBot):
    telegram_id = callback.message.chat.id
    message = messages.MENU_TEXT
    data = get_menu_data()
    keyboard = KeyboardConstructor().create_inline_keyboard(data)

    return bot.send_message(telegram_id, message, reply_markup=keyboard)
