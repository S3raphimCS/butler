from pathlib import Path

from telebot import TeleBot
from telebot.types import CallbackQuery, Message

from butler_core.apps.vpn_configs.models import VpnConfig
from butler_core.bot.handlers.helpers import get_config_menu_data
from butler_core.bot.handlers.menu import menu
from butler_core.bot.utils import messages
from butler_core.bot.utils.error_handler import ErrorHandler
from butler_core.bot.utils.keyboards import KeyboardConstructor


@ErrorHandler.create()
def config_menu(callback: CallbackQuery, bot: TeleBot) -> None:
    """Функция для вывода меню действий с конфигурациями."""
    telegram_id = callback.message.chat.id
    data = get_config_menu_data()
    message = messages.CONFIG_MENU
    keyboard = KeyboardConstructor().create_inline_keyboard(data)
    bot.send_message(telegram_id, message, reply_markup=keyboard)


@ErrorHandler.create()
def get_configs(callback: CallbackQuery, bot: TeleBot) -> None:
    """Функция для получения списка рабочих конфигураций."""
    telegram_id = callback.message.chat.id
    configs = VpnConfig.objects.filter(is_working=True)[:10]
    if configs:
        bot.send_message(telegram_id, "Начинаю отправку конфигов")
        for config in configs:
            bot.send_document(telegram_id, document=Path(config.file.path).open(mode="rb"))
    else:
        bot.send_message(telegram_id, messages.NO_AVAILABLE_CONFIGS)


@ErrorHandler.create()
def config_does_not_work(callback: CallbackQuery, bot: TeleBot) -> None:
    """Функция для пометки конфига нерабочим"""
    telegram_id = callback.message.chat.id
    text = messages.SEND_UNAVAILABLE_CONFIG
    bot.send_message(telegram_id, text)
    return bot.register_next_step_handler_by_chat_id(telegram_id, get_unavailable_config, bot)


@ErrorHandler.create()
def get_unavailable_config(message: Message, bot: TeleBot) -> None:
    telegram_id = message.chat.id
    if hasattr(message, "entities"):
        if message.entities:
            if message.entities[0].type == "bot_command":
                bot.clear_step_handler_by_chat_id(telegram_id)
                if message.text == "/menu":
                    return menu(message, bot)
    if not message.document or message.document.mime_type != "application/x-openvpn-profile":
        message_text = messages.SENT_INCORRECT_DATA
        bot.send_message(telegram_id, message_text)
        return bot.register_next_step_handler_by_chat_id(telegram_id, get_unavailable_config, bot)
    else:
        config = VpnConfig.objects.filter(file__icontains=message.document.file_name).first()
        if config:
            config.is_working = False
            config.save(update_fields=["is_working"])
            message_text = messages.CONFIG_MARKED_AS_UNAVAILABLE
            bot.send_message(telegram_id, message_text)
        else:
            bot.send_message(telegram_id, messages.CONFIG_NOT_FOUND)
            return menu(message, bot)
