from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.callback_data import CallbackData

share_phone_number = KeyboardButton("Accept & share my contact ☎", request_contact=True)
button_message_to_support = KeyboardButton("Message support")

maybe_later = KeyboardButton("Maybe later")
reply_kb_phone_number = (
    ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    .add(share_phone_number)
    .add(button_message_to_support)
    .add(maybe_later)
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

skip_current_flow = InlineKeyboardButton("Cancel", callback_data="skip_flow")
reply_kb_cancel_current_flow = InlineKeyboardMarkup(resize_keyboard=True).add(
    skip_current_flow
)


def get_inline_kb_registration():
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
    return (
        InlineKeyboardMarkup(row_width=4)
        .row(button_yes, button_no)
        .add(button_show_advantages)
        .add(button_change_lang)
    )


def get_transactions_menu():
    button_transaction_number = InlineKeyboardButton(
        "Last Transactions By Number", callback_data="last_n_trans"
    )
    button_transactions_date = InlineKeyboardButton(
        "All Transactions For Dates", callback_data="all_trans_date"
    )
    return (
        InlineKeyboardMarkup(row_width=4)
        .add(button_transaction_number)
        .add(button_transactions_date)
    )


def get_change_profile_menu():
    button_change_first_name = InlineKeyboardButton(
        "Change First name", callback_data="change_first_name"
    )
    button_change_last_name = InlineKeyboardButton(
        "Change Last name", callback_data="change_last_name"
    )
    button_change_country = InlineKeyboardButton(
        "Change my country", callback_data="change_country"
    )
    button_change_lang = InlineKeyboardButton(
        "Change my lang", callback_data="change_lang"
    )
    button_change_currency = InlineKeyboardButton(
        "Change my currency", callback_data="change_currency"
    )
    button_submit_changes = InlineKeyboardButton(
        "All information is correct", callback_data="submit_profile_info"
    )

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
    button_open_store = InlineKeyboardButton(
        "Open shop", callback_data="open_shop"
    )
    button_check_basket = InlineKeyboardButton(
        "Basket", callback_data="check_basket"
    )
    button_check_active_orders = InlineKeyboardButton(
        "Active Orders", callback_data="check_active_orders"
    )
    button_check_finished_order = InlineKeyboardButton(
        "Finished Orders", callback_data="check_finished_orders"
    )
    button_check_profile = InlineKeyboardButton(
        "Check profile", callback_data="check_profile"
    )
    button_discounts = InlineKeyboardButton(
        "Discounts", callback_data="check_discount"
    )
    button_inline_message_to_support = InlineKeyboardButton(
        "Message to support", callback_data="to_support"
    )

    return (
        InlineKeyboardMarkup(row_width=4)
        .add(button_open_store)
        .add(button_check_profile)
        .add(button_check_basket)
        .add(button_check_active_orders)
        .add(button_check_finished_order)
        .add(button_discounts)
        .add(button_inline_message_to_support)

    )


def get_approvement_top_up_balance_menu():
    button_accept_top_up_balance = InlineKeyboardButton(
        "Accept", callback_data="accept_top_up_balance"
    )
    button_decline_top_up_balance = InlineKeyboardButton(
        "Decline", callback_data="decline_top_up_balance"
    )

    return (
        InlineKeyboardMarkup(row_width=4)
        .add(button_accept_top_up_balance)
        .add(button_decline_top_up_balance)
    )


def get_approvement_transaction_to_user_menu():
    button_accept_transaction_to_user = InlineKeyboardButton(
        "Accept", callback_data="accept_transaction_to_user"
    )
    button_decline_transaction_to_user = InlineKeyboardButton(
        "Decline", callback_data="decline_transaction_to_user"
    )

    return (
        InlineKeyboardMarkup(row_width=4)
        .add(button_accept_transaction_to_user)
        .add(button_decline_transaction_to_user)
    )


def get_approvement_withdrawal_menu():
    button_accept_withdrawal = InlineKeyboardButton(
        "Accept", callback_data="accept_withdrawal"
    )
    button_decline_withdrawal = InlineKeyboardButton(
        "Decline", callback_data="decline_withdrawal"
    )

    return (
        InlineKeyboardMarkup(row_width=4)
        .add(button_accept_withdrawal)
        .add(button_decline_withdrawal)
    )