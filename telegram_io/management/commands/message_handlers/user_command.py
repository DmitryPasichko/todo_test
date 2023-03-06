import datetime

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext

from telegram_io.services.user_functions import (
    AdminApi,
)
from telegram_io.telegram_menu.menu import get_user_functions_menu, get_transactions_menu
from telegram_io.telegram_menu import menu as kb
from telegram_io.telegram_menu import forms as kbf
from aiogram.types import InputFile


admin_api = AdminApi()

async def check_profile_balance(msg: types.Message):
    await show_current_balance(msg=msg)


async def show_current_balance(
    msg: types.Message = None,
    callback_query: types.CallbackQuery = None,
    bot: Bot = None,
):
    user_external_id = msg.from_user.id if msg else callback_query.from_user.id
    user = await admin_api.get_user_by_external_id(str(user_external_id))
    message = user.get_current_balance_message()
    if msg:
        await msg.reply(message, reply_markup=get_user_functions_menu())
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.message.chat.id,
            message,
            reply_markup=get_user_functions_menu(),
        )


async def check_profile_info(
    msg: types.Message = None,
    callback_query: types.CallbackQuery = None,
    bot: Bot = None,
):
    user_external_id = msg.from_user.id if msg else callback_query.from_user.id
    user = await admin_api.get_user_by_external_id(str(user_external_id))
    message = user.get_profile_info()
    if msg:
        await msg.reply(message, reply_markup=get_user_functions_menu())
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.message.chat.id,
            message,
            reply_markup=get_user_functions_menu(),
        )


async def transaction_to_user(
    msg: types.Message = None,
    callback_query: types.CallbackQuery = None,
    bot: Bot = None,
):
    await bot.answer_callback_query(callback_query.id)
    message = "Enter phone number"
    await bot.send_message(callback_query.message.chat.id, message)
    await kbf.TransactionToUserPaymentForm.phone.set()


async def message_to_support(
    msg: types.Message = None,
    callback_query: types.CallbackQuery = None,
    bot: Bot = None,
):
    message = "Send message to Support"
    if msg:
        await msg.reply(message, reply_markup=get_user_functions_menu())
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.message.chat.id,
            message,
            reply_markup=get_user_functions_menu(),
        )


async def get_transactions(callback_query: types.CallbackQuery = None, bot: Bot = None):
    message = "Choose option for getting transactions"
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.message.chat.id, message, reply_markup=get_transactions_menu()
    )


async def set_number_for_getting_transactions(
    callback_query: types.CallbackQuery, bot: Bot = None
):
    message = "Set count for getting last transactions.\nOnly integer value.\nE.g. `1`"
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, message)
    await kbf.GetTransactionsReportByCount.count.set()


async def get_last_n_transactions(msg: types.Message, state: FSMContext):
    count = "".join(msg.text.split())
    if not count.isdigit() or count.isdigit() < 1:
        await msg.bot.send_message(msg.chat.id, "Wrong data,\nPlease enter valid data")
        return
    user = await admin_api.get_user_by_external_id(str(msg.from_user.id))
    trans = None
    report = None
    await msg.bot.send_document(
        msg.chat.id, InputFile(report, f"transactions_last_{count}.pdf")
    )
    await state.finish()


async def process_transactions_report_by_date(
    callback_query: types.CallbackQuery, bot: Bot = None
):
    message = "Set Start Date for getting last transactions.\nOnly Date format.\nE.g. `2021-10-01`"
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, message)
    await kbf.GetTransactionsReportByDate.date_from.set()


async def set_date_from_transactions_report_by_date(
    msg: types.Message, state: FSMContext
):
    date_from = "".join(msg.text.split())
    try:
        date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
    except Exception:
        await msg.bot.send_message(msg.chat.id, "Wrong data,\nPlease enter valid data")
        return
    if date_from > datetime.date.today():
        await msg.bot.send_message(
            msg.chat.id,
            "Start Date can not be greater than today,\nPlease enter less date",
        )
        return
    async with state.proxy() as proxy:
        proxy["date_from"] = date_from
    message = "Set End Date for getting last transactions.\nOnly Date format.\nE.g. `2021-10-01`"
    await msg.bot.send_message(msg.chat.id, message)
    await kbf.GetTransactionsReportByDate.next()


async def set_date_to_transactions_report_by_date(
    msg: types.Message, state: FSMContext
):
    date_to = "".join(msg.text.split())
    try:
        date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
    except Exception as e:
        await msg.bot.send_message(msg.chat.id, "Wrong data,\nPlease enter valid data")
        return
    if date_to > datetime.date.today():
        await msg.bot.send_message(
            msg.chat.id,
            "End Date can not be greater than today,\nPlease enter less date",
        )
        return
    async with state.proxy() as proxy:
        proxy["date_to"] = date_to
        user = await admin_api.get_user_by_external_id(str(msg.from_user.id))
        trans = None
        report = None
        await msg.bot.send_document(
            msg.chat.id,
            InputFile(
                report, f"transactions_{proxy['date_from']}-{proxy['date_to']}.pdf"
            ),
        )
        await state.finish()


def register_handlers_user_functions(dp: Dispatcher, bot: Bot):
    dp.register_message_handler(check_profile_balance, commands="open_shop")

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("open_shop"))
    async def check_profile_balance_inline(
        callback_query: types.CallbackQuery, bot: Bot = bot
    ):
        await show_current_balance(callback_query=callback_query, bot=bot)

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("check_profile"))
    async def check_profile_info_inline(
        callback_query: types.CallbackQuery, bot: Bot = bot
    ):
        await check_profile_info(callback_query=callback_query, bot=bot)

    @dp.callback_query_handler(
        lambda c: c.data and c.data.startswith("check_active_orders")
    )
    async def transaction_to_user_inline(
        callback_query: types.CallbackQuery, bot: Bot = bot
    ):
        await transaction_to_user(callback_query=callback_query, bot=bot)

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("check_finished_orders"))
    async def message_to_support_inline(
        callback_query: types.CallbackQuery, bot: Bot = bot
    ):
        await message_to_support(callback_query=callback_query, bot=bot)

    @dp.callback_query_handler(
        lambda c: c.data and c.data.startswith("check_basket")
    )
    async def process_get_transactions(
        callback_query: types.CallbackQuery, bot: Bot = bot
    ):
        await get_transactions(callback_query=callback_query, bot=bot)

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("check_discount"))
    async def set_number_for_getting_transactions_inline(
        callback_query: types.CallbackQuery, bot: Bot = bot
    ):
        await set_number_for_getting_transactions(
            callback_query=callback_query, bot=bot
        )

    dp.register_message_handler(
        get_last_n_transactions, state=kbf.GetTransactionsReportByCount.count
    )

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("to_support"))
    async def process_transactions_report_by_date_inline(
        callback_query: types.CallbackQuery, bot: Bot = bot
    ):
        await process_transactions_report_by_date(
            callback_query=callback_query, bot=bot
        )

    dp.register_message_handler(
        set_date_from_transactions_report_by_date,
        state=kbf.GetTransactionsReportByDate.date_from,
    )
    dp.register_message_handler(
        set_date_to_transactions_report_by_date,
        state=kbf.GetTransactionsReportByDate.date_to,
    )
