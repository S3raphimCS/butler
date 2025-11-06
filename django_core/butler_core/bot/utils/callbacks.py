import enum


class Callback(enum.Enum):
    """Перечисление колбеков."""

    GET_CONFIG = "get_config"
    CONFIG_DOESNT_WORK = "config_doesnt_work"
    MENU = "menu"
