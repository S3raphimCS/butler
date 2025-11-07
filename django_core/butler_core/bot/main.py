import logging

from django.conf import settings
from telebot import TeleBot, logger

from butler_core.bot.handlers.configs import (
    config_does_not_work,
    config_menu,
    get_configs,
)
from butler_core.bot.handlers.mailings import mailing_menu, toggle_mailing_subscription
from butler_core.bot.handlers.menu import menu, menu_callback
from butler_core.bot.handlers.start import start
from butler_core.bot.handlers.unknown_command import unknown_command
from butler_core.bot.utils.callbacks import Callback


logger = logger
logger.setLevel(logging.DEBUG)

bot = TeleBot(
    settings.BOT_TOKEN,
    parse_mode='HTML',
)

MESSAGE_HANDLERS_MAP = {
    start: {
        'commands': ['start'],
    },
    menu: {
        "commands": ["menu"],
    },
    unknown_command: {
        "content_types": ["text"],
    },
}

PRE_CHECKOUT_HANDLERS_MAP = {

}

CALLBACK_HANDLERS_MAP = {
    get_configs: {
        "func": lambda callback: callback.data == Callback.GET_CONFIG.value
    },
    config_does_not_work: {
        "func": lambda callback: callback.data == Callback.CONFIG_DOESNT_WORK.value
    },
    menu_callback: {
        "func": lambda callback: callback.data == Callback.MENU.value
    },
    config_menu: {
        "func": lambda callback: callback.data == Callback.CONFIG_MENU.value
    },
    mailing_menu: {
        "func": lambda callback: callback.data == Callback.MAILING_MENU.value
    },
    toggle_mailing_subscription: {
        "func": lambda callback: callback.data == Callback.MAILING_TOGGLE_SUBSCRIBE.value
    },
}


def register_handlers():
    """Функция регистрации обработчиков бота."""
    for func, params in MESSAGE_HANDLERS_MAP.items():
        bot.register_message_handler(
            func,
            **params,
            pass_bot=True,
        )

    for func, params in CALLBACK_HANDLERS_MAP.items():
        bot.register_callback_query_handler(
            func,
            **params,
            pass_bot=True,
        )

    for func, params in PRE_CHECKOUT_HANDLERS_MAP.items():
        bot.register_pre_checkout_query_handler(
            func,
            **params,
            pass_bot=True,
        )


register_handlers()
