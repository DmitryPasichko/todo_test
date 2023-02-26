from aiogram import Dispatcher, types
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext

from telegram_io.telegram_menu.menu import get_user_functions_menu


async def process_help_command(msg: types.Message):
    await msg.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


async def skip_current_flow(
    callback_query: types.CallbackQuery = None,
    state: FSMContext = None,
    bot: Bot = None,
):
    await state.finish()
    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text="Operation is cancelled",
        reply_markup=get_user_functions_menu(),
    )


def register_handlers_system(dp: Dispatcher, bot: Bot):
    dp.register_message_handler(process_help_command, commands="help")

    @dp.callback_query_handler(
        lambda c: c.data and c.data.startswith("skip_flow"), state="*"
    )
    async def skip_current_flow_inline(
        callback_query: types.CallbackQuery, state: FSMContext, bot: Bot = bot
    ):
        await skip_current_flow(callback_query=callback_query, bot=bot, state=state)
