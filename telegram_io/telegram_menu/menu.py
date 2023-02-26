from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.callback_data import CallbackData

button_yes = InlineKeyboardButton(
    "Yes, I want to sign up", callback_data="registration"
)
button_no = InlineKeyboardButton(
    "No, close and exit", callback_data="decline_registration"
)
button_show_advantages = InlineKeyboardButton(
    "Show me Gallant Clothes advantages", callback_data="show_advantages"
)
button_change_lang = InlineKeyboardButton(
    "Change Language", callback_data="change_language"
)
inline_kb_registration = (
    InlineKeyboardMarkup(row_width=4)
    .row(button_yes, button_no)
    .add(button_show_advantages)
    .add(button_change_lang)
)

share_phone_number = KeyboardButton("Accept & share my contact ☎", request_contact=True)
button_message_to_support = KeyboardButton("Message support")
button_inline_message_to_support = InlineKeyboardButton(
    "Message to support", callback_data="to_support"
)
maybe_later = KeyboardButton("Maybe later")
reply_kb_phone_number = (
    ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    .add(share_phone_number)
    .add(button_message_to_support)
    .add(maybe_later)
)

button_change_first_name = InlineKeyboardButton(
    "Change First name", callback_data="change_first_name"
)
button_change_last_name = InlineKeyboardButton(
    "Change Last name", callback_data="change_last_name"
)
button_change_phone = InlineKeyboardButton(
    "Change my phone number", callback_data="change_phone"
)
button_change_country = InlineKeyboardButton(
    "Change my country", callback_data="change_country"
)
button_change_lang = InlineKeyboardButton("Change my lang", callback_data="change_lang")
button_change_currency = InlineKeyboardButton(
    "Change my currency", callback_data="change_currency"
)
button_submit_changes = InlineKeyboardButton(
    "All information is correct", callback_data="submit_profile_info"
)

profile_change_commands = {
    "change_first_name": "first_name",
    "change_last_name": "last_name",
    "change_phone": "phone_number",
    "change_country": "country",
    "change_lang": "language",
    "change_currency": "balance",
}
profile_cb = CallbackData(
    "profile", "action", "phone", "country", "lang", "main_currency"
)
button_check_balance = InlineKeyboardButton(
    "Check balance", callback_data="check_balance"
)
button_check_profile = InlineKeyboardButton(
    "Check profile", callback_data="check_profile"
)
button_top_up_balance = InlineKeyboardButton(
    "Top up balance", callback_data="top_up_balance"
)
button_transaction_to_user = InlineKeyboardButton(
    "Transaction to user", callback_data="transaction_to_user"
)
button_withdrawal = InlineKeyboardButton("Withdrawal", callback_data="withdrawal")
button_transactions = InlineKeyboardButton(
    "My Transactions", callback_data="get_transactions"
)

button_transaction_number = InlineKeyboardButton(
    "Last Transactions By Number", callback_data="last_n_trans"
)
button_transactions_date = InlineKeyboardButton(
    "All Transactions For Dates", callback_data="all_trans_date"
)

skip_current_flow = InlineKeyboardButton("Cancel", callback_data="skip_flow")
reply_kb_cancel_current_flow = InlineKeyboardMarkup(resize_keyboard=True).add(
    skip_current_flow
)


def get_transactions_menu():
    return (
        InlineKeyboardMarkup(row_width=4)
        .add(button_transaction_number)
        .add(button_transactions_date)
    )


def get_change_profile_menu():
    return (
        InlineKeyboardMarkup(row_width=4)
        .add(button_change_first_name)
        .add(button_change_last_name)
        .add(button_change_country)
        .add(button_change_lang)
        .add(button_change_currency)
        .add(button_submit_changes)
    )


def get_user_functions_menu():
    return (
        InlineKeyboardMarkup(row_width=4)
        .add(button_check_balance)
        .add(button_check_profile)
        .add(button_top_up_balance)
        .add(button_transaction_to_user)
        .add(button_withdrawal)
        .add(button_inline_message_to_support)
        .add(button_transactions)
    )


class RegisterForm(StatesGroup):
    start = State()
    first_name = State()
    last_name = State()
    phone = State()
    country = State()
    language = State()
    balance = State()
    submit = State()


class TopUpBalancePaymentForm(StatesGroup):
    amount = State()
    card_number = State()
    expire_month = State()
    expire_year = State()
    cvv = State()
    submit = State()


button_accept_top_up_balance = InlineKeyboardButton(
    "Accept", callback_data="accept_top_up_balance"
)
button_decline_top_up_balance = InlineKeyboardButton(
    "Decline", callback_data="decline_top_up_balance"
)


def get_approvement_top_up_balance_menu():
    return (
        InlineKeyboardMarkup(row_width=4)
        .add(button_accept_top_up_balance)
        .add(button_decline_top_up_balance)
    )


class WithdrawalPaymentForm(StatesGroup):
    amount = State()
    card_number = State()
    expire_month = State()
    expire_year = State()
    submit = State()


button_accept_transaction_to_user = InlineKeyboardButton(
    "Accept", callback_data="accept_transaction_to_user"
)
button_decline_transaction_to_user = InlineKeyboardButton(
    "Decline", callback_data="decline_transaction_to_user"
)


def get_approvement_transaction_to_user_menu():
    return (
        InlineKeyboardMarkup(row_width=4)
        .add(button_accept_transaction_to_user)
        .add(button_decline_transaction_to_user)
    )


class TransactionToUserPaymentForm(StatesGroup):
    phone = State()
    amount = State()
    submit = State()


button_accept_withdrawal = InlineKeyboardButton(
    "Accept", callback_data="accept_withdrawal"
)
button_decline_withdrawal = InlineKeyboardButton(
    "Decline", callback_data="decline_withdrawal"
)


def get_approvement_withdrawal_menu():
    return (
        InlineKeyboardMarkup(row_width=4)
        .add(button_accept_withdrawal)
        .add(button_decline_withdrawal)
    )


class GetTransactionsReportByCount(StatesGroup):
    count = State()


class GetTransactionsReportByDate(StatesGroup):
    date_from = State()
    date_to = State()
