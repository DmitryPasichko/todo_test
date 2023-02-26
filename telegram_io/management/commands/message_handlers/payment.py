import decimal

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from checkout_sdk.common.enums import Currency

from RaccoonPayWebService.services.payment import (
    flow_transaction_between_users,
    flow_transaction_top_up_balance,
)
from RaccoonPayWebService.services.payment_utils import get_comission_fee_for_payment
from RaccoonPayWebService.services.user_functions import (
    find_user_by_phone_number,
    find_user_by_external_id,
)
from RaccoonPayWebService.services.validation import validate_phone_international
from RaccoonPayWebService.utils.phone import normalize_phone_number
from telegram.telegram_menu import menu as kb
from telegram.telegram_menu.menu import (
    get_approvement_transaction_to_user_menu,
    get_user_functions_menu,
    reply_kb_cancel_current_flow,
    get_approvement_top_up_balance_menu,
)


async def process_top_up_balance(
    msg: types.Message = None,
    callback_query: types.CallbackQuery = None,
    bot: Bot = None,
):
    message = "How much money do you want to transfer to your balance?\nE.g.: `1`"
    if msg:
        await msg.reply(message)
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.message.chat.id,
            message,
            reply_markup=reply_kb_cancel_current_flow,
        )
    await kb.TopUpBalancePaymentForm.amount.set()


async def process_amount_top_up_balance(message: types.Message, state: FSMContext):
    amount = "".join(message.text.split())
    if not amount.isdigit():
        await message.bot.send_message(
            message.chat.id, "Wrong data,\nPlease enter valid data"
        )
        return
    async with state.proxy() as proxy:
        proxy["amount"] = int(message.text)
    await kb.TopUpBalancePaymentForm.next()
    to_user = await find_user_by_external_id(str(message.from_user.id))
    commission = await get_comission_fee_for_payment(
        to_user.balance, amount=amount, tx_type=1
    )
    await message.reply(
        f"Commission for this operation: {commission} {to_user.balance}",
        reply_markup=get_approvement_top_up_balance_menu(),
    )
    await message.answer(
        "If you want to proceed please enter your card number.\nE.g: `1234 1234 1234 1234`"
    )


async def process_card_number_top_up_balance(message: types.Message, state: FSMContext):
    card_number = "".join(message.text.split())
    if not card_number.isdigit() or len(card_number) != 16:
        await message.bot.send_message(
            message.chat.id, "Wrong data,\nPlease enter valid data"
        )
        return
    async with state.proxy() as proxy:
        proxy["card_number"] = card_number
    await kb.TopUpBalancePaymentForm.next()
    await message.reply("Enter expire month.\nE.g.: `1`,`12`")


async def process_expire_month_top_up_balance(
    message: types.Message, state: FSMContext
):
    month = "".join(message.text.split())
    if not month.isdigit() or 0 > int(month) > 12 or 0 > len(month) > 2:
        await message.bot.send_message(
            message.chat.id, "Wrong data,\nPlease enter valid data"
        )
        return
    async with state.proxy() as proxy:
        proxy["expire_month"] = int(month)
    await kb.TopUpBalancePaymentForm.next()
    await message.reply("Enter expire year.\nE.g.: `2021`")


async def process_expire_year_top_up_balance(message: types.Message, state: FSMContext):
    year = "".join(message.text.split())
    if not year.isdigit() or len(year) != 4:
        await message.bot.send_message(
            message.chat.id, "Wrong data,\nPlease enter valid data"
        )
        return
    async with state.proxy() as proxy:
        proxy["expire_year"] = int(year)
    await kb.TopUpBalancePaymentForm.next()
    await message.reply("Enter cvv.\nE.g.: `123`")


async def process_cvv_top_up_balance(message: types.Message, state: FSMContext):
    cvv = "".join(message.text.split())
    if not cvv.isdigit() or len(cvv) != 3:
        await message.bot.send_message(
            message.chat.id, "Wrong data,\nPlease enter valid data"
        )
        return
    async with state.proxy() as proxy:
        proxy["cvv"] = cvv
    await kb.TopUpBalancePaymentForm.next()
    result = {}
    async with state.proxy() as proxy:
        to_user = await find_user_by_external_id(str(message.from_user.id))
        try:
            result = await flow_transaction_top_up_balance(
                to_user=to_user,
                amount=proxy["amount"],
                currency=Currency.USD,
                payout_kwargs=proxy,
            )
        except Exception as e:
            await message.answer(str(e), reply_markup=get_user_functions_menu())
    if result:
        if result.get("stage") == 4:
            message_text = f"Top Up Balance operation is waiting for approve.\nPlease follow link below \n{result.get('url')}"
        if result.get("stage") == 2:
            message_text = "Balance has been successfully replenished"
    else:
        message_text = "System issue.Please try later"
    await state.finish()
    await message.bot.send_message(
        message.chat.id, message_text, reply_markup=get_user_functions_menu()
    )


async def decline_flow_top_up_balance(
    callback_query: types.CallbackQuery, state: FSMContext, bot=Bot
):
    await state.finish()
    message = "Operation declined"
    await bot.send_message(
        callback_query.message.chat.id, message, reply_markup=get_user_functions_menu()
    )


async def process_phone_transaction_to_user(message: types.Message, state: FSMContext):
    validated = validate_phone_international(message.text)
    if not validated:
        await message.bot.send_message(
            message.chat.id, "Wrong data,\nPlease enter valid data"
        )
        return
    phone = normalize_phone_number(message.text)
    to_user = await find_user_by_phone_number(phone)
    if not to_user:
        await message.bot.send_message(
            message.chat.id, "There is not user with this phone.\nPlease try again"
        )
        await state.finish()
        return
    user = await find_user_by_external_id(str(message.from_user.id))
    if user.id == to_user.id:
        await message.bot.send_message(
            message.chat.id, "You can't create transactions to yourself"
        )
        await state.finish()
        return
    await state.update_data({"phone": phone, "to_user": to_user})

    await message.answer(
        "Enter amount.\nE.g.: `1`", reply_markup=reply_kb_cancel_current_flow
    )
    await kb.TransactionToUserPaymentForm.amount.set()


async def process_amount_transaction_to_user(message: types.Message, state: FSMContext):
    amount = "".join(message.text.split())
    if not amount.isdigit() or int(amount) < 1:
        await message.bot.send_message(
            message.chat.id, "Wrong data,\nPlease enter valid data"
        )
        return
    await state.update_data({"amount": message.text})
    to_user = await find_user_by_external_id(str(message.from_user.id))
    commission = await get_comission_fee_for_payment(
        to_user.balance, amount=amount, tx_type=1
    )
    await kb.TransactionToUserPaymentForm.next()
    await message.answer(
        f"Commission got this operation: {commission}.\nAccept or Decline operation",
        reply_markup=get_approvement_transaction_to_user_menu(),
    )


async def process_flow_transaction_between_users(
    callback_query: types.CallbackQuery, state: FSMContext, bot=Bot
):
    async with state.proxy() as proxy:
        from_user = await find_user_by_external_id(callback_query.from_user.id)
        try:
            await flow_transaction_between_users(
                from_user,
                proxy["to_user"],
                decimal.Decimal(proxy["amount"]),
                from_user.balance,
            )
        except Exception as e:
            await callback_query.message.answer(str(e))
            return
        finally:
            await state.finish()
        await state.finish()
        message = "Transaction successfully created"
        message_to_user = (
            f"{from_user.first_name + from_user.last_name} has sent transaction to you"
        )
        proxy["to_user"]
        await bot.send_message(
            proxy["to_user"].main_messenger.external_user_id,
            message_to_user,
            reply_markup=get_user_functions_menu(),
        )
        await bot.send_message(
            callback_query.message.chat.id,
            message,
            reply_markup=get_user_functions_menu(),
        )


async def decline_flow_transaction_between_users(
    callback_query: types.CallbackQuery, state: FSMContext, bot=Bot
):
    await state.finish()
    message = "Transaction declined"
    await bot.send_message(
        callback_query.message.chat.id, message, reply_markup=get_user_functions_menu()
    )


def register_handlers_payment(dp: Dispatcher, bot: Bot):
    dp.register_message_handler(
        process_amount_top_up_balance, state=kb.TopUpBalancePaymentForm.amount
    )
    dp.register_message_handler(
        process_card_number_top_up_balance, state=kb.TopUpBalancePaymentForm.card_number
    )
    dp.register_message_handler(
        process_expire_month_top_up_balance,
        state=kb.TopUpBalancePaymentForm.expire_month,
    )
    dp.register_message_handler(
        process_expire_year_top_up_balance, state=kb.TopUpBalancePaymentForm.expire_year
    )
    dp.register_message_handler(
        process_cvv_top_up_balance, state=kb.TopUpBalancePaymentForm.cvv
    )
    dp.register_message_handler(
        process_phone_transaction_to_user, state=kb.TransactionToUserPaymentForm.phone
    )
    dp.register_message_handler(
        process_amount_transaction_to_user, state=kb.TransactionToUserPaymentForm.amount
    )

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("top_up_balance"))
    async def top_up_balance_inline(
        callback_query: types.CallbackQuery, bot: Bot = bot
    ):
        await process_top_up_balance(callback_query=callback_query, bot=bot)

    @dp.callback_query_handler(
        lambda c: c.data and c.data.startswith("accept_transaction_to_user"),
        state=kb.TransactionToUserPaymentForm.submit,
    )
    async def accept_transaction_between_users_inline(
        callback_query: types.CallbackQuery,
        state=kb.TransactionToUserPaymentForm.submit,
        bot: Bot = bot,
    ):
        await process_flow_transaction_between_users(
            callback_query=callback_query, state=state, bot=bot
        )

    @dp.callback_query_handler(
        lambda c: c.data and c.data.startswith("decline_transaction_to_user"),
        state=kb.TransactionToUserPaymentForm.submit,
    )
    async def decline_transaction_between_users_inline(
        callback_query: types.CallbackQuery,
        state=kb.TransactionToUserPaymentForm.submit,
        bot: Bot = bot,
    ):
        await decline_flow_transaction_between_users(
            callback_query=callback_query, state=state, bot=bot
        )

    @dp.callback_query_handler(
        lambda c: c.data and c.data.startswith("decline_top_up_balance"),
        state=kb.TransactionToUserPaymentForm.submit,
    )
    async def decline_transaction_top_up_balance(
        callback_query: types.CallbackQuery,
        state=kb.TopUpBalancePaymentForm.submit,
        bot: Bot = bot,
    ):
        await decline_flow_top_up_balance(
            callback_query=callback_query, state=state, bot=bot
        )
