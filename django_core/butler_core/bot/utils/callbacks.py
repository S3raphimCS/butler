import enum


class Callback(enum.Enum):
    """Перечисление колбеков."""

    MENU = "menu"

    GET_CONFIG = "get_config"
    CONFIG_DOESNT_WORK = "config_doesnt_work"

    CONFIG_MENU = "config_menu"
    MAILING_MENU = "mailing_menu"
    GET_SPECIFIC_COUNTRY_CONFIGS = "get_specific_country_configs"
    CHOOSE_SPECIFIC_COUNTRY_CONFIG = "choose_specific_country_config"

    MAILING_TOGGLE_SUBSCRIBE = "mailing_toggle"
