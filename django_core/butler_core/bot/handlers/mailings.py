from telebot import TeleBot
from telebot.types import CallbackQuery

from butler_core.apps.mailing.models import MailingSubscription
from butler_core.apps.users.models import BotUser
from butler_core.bot.handlers.helpers import get_mailing_menu_data
from butler_core.bot.utils import buttons, messages
from butler_core.bot.utils.callbacks import Callback
from butler_core.bot.utils.error_handler import ErrorHandler
from butler_core.bot.utils.keyboards import KeyboardConstructor


@ErrorHandler.create()
def mailing_menu(callback: CallbackQuery, bot: TeleBot) -> None:
    """Меню рассылок"""
    telegram_id = callback.message.chat.id
    data = get_mailing_menu_data()
    message = messages.MAILING_MENU
    keyboard = KeyboardConstructor().create_inline_keyboard(data)
    bot.send_message(telegram_id, message, reply_markup=keyboard)


@ErrorHandler.create()
def toggle_mailing_subscription(callback: CallbackQuery, bot: TeleBot) -> None:
    """Подписаться/отписаться от рассылки"""
    telegram_id = callback.message.chat.id
    user = BotUser.objects.get(telegram_id=telegram_id)
    subscription, created = MailingSubscription.objects.get_or_create(user=user)
    if created:
        message = messages.MAILING_SUBSCRIBE
    else:
        if subscription.is_active:
            message = messages.MAILING_UNSUBSCRIBE
        else:
            message = messages.MAILING_SUBSCRIBE
        subscription.is_active = not subscription.is_active
        subscription.save(update_fields=['is_active'])
    data = {buttons.MAILINGS: Callback.MAILING_MENU.value}
    keyboard = KeyboardConstructor().create_inline_keyboard(data)
    bot.send_message(telegram_id, message, reply_markup=keyboard)
