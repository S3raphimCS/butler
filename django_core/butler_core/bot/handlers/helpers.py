from butler_core.bot.utils import buttons
from butler_core.bot.utils.callbacks import Callback


def get_start_data() -> dict:
    """Получение кнопок после регистрации клиента."""
    callback_data = {
        buttons.GET_CONFIG: Callback.GET_CONFIG.value,
    }
    return callback_data


def get_menu_data() -> dict:
    """Получение кнопок меню"""
    callback_data = {
        buttons.CONFIGS: Callback.CONFIG_MENU.value,
        buttons.MAILINGS: Callback.MAILING_MENU.value,
    }
    return callback_data


def get_config_menu_data() -> dict:
    """Получение кнопок меню конфигураций"""
    callback_data = {
        buttons.GET_CONFIG: Callback.GET_CONFIG.value,
        buttons.CONFIG_DOESNT_WORK: Callback.CONFIG_DOESNT_WORK.value,
        buttons.MENU: Callback.MENU.value,
    }
    return callback_data


def get_mailing_menu_data() -> dict:
    """Получение кнопок меню рассылок"""
    callback_data = {
        buttons.MAILING_SUBSCRIPTION: Callback.MAILING_TOGGLE_SUBSCRIBE.value,
        buttons.MENU: Callback.MENU.value,
    }
    return callback_data
