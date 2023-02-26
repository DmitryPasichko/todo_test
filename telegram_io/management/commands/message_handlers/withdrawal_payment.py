import decimal

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from checkout_sdk.common.enums import Currency

from RaccoonPayWebService.services.payment import flow_transaction_withdrawal
from RaccoonPayWebService.services.user_functions import find_user_by_external_id
from telegram.telegram_menu import menu as kb
from telegram.telegram_menu.menu import (
    get_approvement_withdrawal_menu,
    get_user_functions_menu,
    reply_kb_cancel_current_flow,
)


async def process_withdrawal(
    msg: types.Message = None,
    callback_query: types.CallbackQuery = None,
    bot: Bot = None,
):
    message = "How much money do you want to withdrawal?\nE.g.: `1`"
    if msg:
        await msg.reply(message)
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.message.chat.id,
            message,
            reply_markup=reply_kb_cancel_current_flow,
        )
    await kb.WithdrawalPaymentForm.amount.set()


async def process_amount_withdrawal(message: types.Message, state: FSMContext):
    amount = "".join(message.text.split())
    if not amount.isdigit():
        await message.bot.send_message(
            message.chat.id, "Wrong data,\nPlease enter valid data"
        )
        return
    async with state.proxy() as proxy:
        proxy["amount"] = int(message.text)
    await kb.WithdrawalPaymentForm.next()
    await message.reply("Enter your card number.\nE.g: `1234 1234 1234 1234`")


async def process_card_number_withdrawal(message: types.Message, state: FSMContext):
    card_number = "".join(message.text.split())
    if not card_number.isdigit() or len(card_number) != 16:
        await message.bot.send_message(
            message.chat.id, "Wrong data,\nPlease enter valid data"
        )
        return
    async with state.proxy() as proxy:
        proxy["card_number"] = card_number
    await kb.WithdrawalPaymentForm.next()
    await message.reply("Enter expire month.\nE.g.: `1`,`12`")


async def process_expire_month_withdrawal(message: types.Message, state: FSMContext):
    month = "".join(message.text.split())
    if not month.isdigit() or 0 > int(month) > 12 or 0 > len(month) > 2:
        await message.bot.send_message(
            message.chat.id, "Wrong data,\nPlease enter valid data"
        )
        return
    async with state.proxy() as proxy:
        proxy["expire_month"] = int(month)
    await kb.WithdrawalPaymentForm.next()
    await message.reply("Enter expire year.\nE.g.: `2021`")


async def process_expire_year_withdrawal(message: types.Message, state: FSMContext):
    year = "".join(message.text.split())
    if not year.isdigit() or len(year) != 4:
        await message.bot.send_message(
            message.chat.id, "Wrong data,\nPlease enter valid data"
        )
        return
    async with state.proxy() as proxy:
        proxy["expire_year"] = int(year)
    await kb.WithdrawalPaymentForm.next()
    await message.answer(
        "Accept or Decline operation", reply_markup=get_approvement_withdrawal_menu()
    )


async def accept_withdrawal(
    callback_query: types.CallbackQuery, state: FSMContext, bot=Bot
):
    async with state.proxy() as proxy:
        from_user = await find_user_by_external_id(callback_query.from_user.id)
        try:
            await flow_transaction_withdrawal(
                from_user,
                decimal.Decimal(proxy["amount"]),
                Currency.USD,
                payout_kwargs=proxy,
            )
        except Exception as e:
            await callback_query.message.answer(str(e))
            return
        finally:
            await state.finish()
        await state.finish()
        message = "Transaction successfully created"
        await bot.send_message(
            callback_query.message.chat.id,
            message,
            reply_markup=get_user_functions_menu(),
        )


async def decline_withdrawal(
    callback_query: types.CallbackQuery, state: FSMContext, bot=Bot
):
    await state.finish()
    message = "Operation is declined"
    await bot.send_message(
        callback_query.message.chat.id, message, reply_markup=get_user_functions_menu()
    )


def register_handlers_withdrawal(dp: Dispatcher, bot: Bot):
    dp.register_message_handler(
        process_amount_withdrawal, state=kb.WithdrawalPaymentForm.amount
    )
    dp.register_message_handler(
        process_card_number_withdrawal, state=kb.WithdrawalPaymentForm.card_number
    )
    dp.register_message_handler(
        process_expire_month_withdrawal, state=kb.WithdrawalPaymentForm.expire_month
    )
    dp.register_message_handler(
        process_expire_year_withdrawal, state=kb.WithdrawalPaymentForm.expire_year
    )

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("withdrawal"))
    async def withdrawal_inline(callback_query: types.CallbackQuery, bot: Bot = bot):
        await process_withdrawal(callback_query=callback_query, bot=bot)

    @dp.callback_query_handler(
        lambda c: c.data and c.data.startswith("accept_withdrawal"),
        state=kb.WithdrawalPaymentForm.submit,
    )
    async def accept_transaction_between_users_inline(
        callback_query: types.CallbackQuery,
        state=kb.WithdrawalPaymentForm.submit,
        bot: Bot = bot,
    ):
        await accept_withdrawal(callback_query=callback_query, state=state, bot=bot)

    @dp.callback_query_handler(
        lambda c: c.data and c.data.startswith("decline_withdrawal"),
        state=kb.TransactionToUserPaymentForm.submit,
    )
    async def decline_transaction_between_users_inline(
        callback_query: types.CallbackQuery,
        state=kb.WithdrawalPaymentForm.submit,
        bot: Bot = bot,
    ):
        await decline_withdrawal(callback_query=callback_query, state=state, bot=bot)
