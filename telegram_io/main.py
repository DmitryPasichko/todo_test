import os
import dotenv
import logging
from functools import wraps

import aiogram.dispatcher.handler as handler
from aiogram import Bot, Dispatcher, executor
from aiogram.types import CallbackQuery, Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from django.utils import translation

from services.user_functions import AdminApi

from management.commands.message_handlers.system import register_handlers_system
# from management.commands.message_handlers.payment import register_handlers_payment
from management.commands.message_handlers.registration import register_handlers_registration
from management.commands.message_handlers.user_command import register_handlers_user_functions
# from management.commands.message_handlers.withdrawal_payment import register_handlers_withdrawal

dotenv.load_dotenv()
logger = logging.getLogger("Bot INIT")
admin_api = AdminApi()

def get_bot_instance():
    return Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))


def user_language(func):
    old_lang = translation.get_language()

    @wraps(func)
    async def wrapped(bot, *args, **kwargs):
        new_lang = old_lang
        user_id = None
        user = None
        if args:
            if isinstance(args[0], CallbackQuery):
                user_id = args[0].from_user.id
            elif isinstance(args[0], Message):
                user_id = args[0].from_user.id
            if user_id:
                user = await admin_api.get_user_by_external_id(str(user_id))
            if user:
                new_lang = 'ru'  # user.language
            translation.activate(new_lang)
        result = await func(bot, *args, **kwargs)
        return result

    translation.activate(old_lang)
    return wrapped


if __name__ == '__main__':
    # handler.Handler.notify = user_language(handler.Handler.notify)

    storage = MemoryStorage()
    bot = get_bot_instance()
    dp = Dispatcher(bot, storage=storage)

    register_handlers_system(dp, bot)
    register_handlers_registration(dp, bot)
    register_handlers_user_functions(dp, bot)
    # register_handlers_payment(dp, bot)
    # register_handlers_withdrawal(dp, bot)
    logger.info("BOT is RUNNING")
    executor.start_polling(
        dp,
        skip_updates=True
    )
    logger.info("BOT is down")
