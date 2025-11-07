import enum


class Callback(enum.Enum):
    """Перечисление колбеков."""

    MENU = "menu"

    GET_CONFIG = "get_config"
    CONFIG_DOESNT_WORK = "config_doesnt_work"

    CONFIG_MENU = "config_menu"
    MAILING_MENU = "mailing_menu"

    MAILING_TOGGLE_SUBSCRIBE = "mailing_toggle"
