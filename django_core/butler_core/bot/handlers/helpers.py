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
        buttons.GET_CONFIG: Callback.GET_CONFIG.value,
        buttons.CONFIG_DOESNT_WORK: Callback.CONFIG_DOESNT_WORK.value,
    }
    return callback_data
