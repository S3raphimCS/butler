from butler_core.bot.utils import buttons
from butler_core.bot.utils.callbacks import Callback


def get_start_data() -> dict:
    """Получение кнопок после регистрации клиента."""
    callback_data = {
        buttons.PLAY: Callback.QUESTS.value,
        buttons.JUST_CHECK: Callback.SOCIALS.value,
    }
    return callback_data