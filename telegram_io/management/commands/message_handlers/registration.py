from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State

# from RaccoonPayWebService.models.client_profile import Profile
from telegram_io.services.registration import (
    get_welcome_message,
    get_welcome_back_message_for_user,
    get_agree_registration_message,
    get_or_register_user,
)
from telegram_io.services.user_functions import AdminApi
from telegram_io.services.validation import profile_validate_field
from telegram_io.utils.phone import (
    normalize_phone_number,
    get_country_by_phone,
)
from telegram_io.telegram_menu import menu as kb
from telegram_io.telegram_menu import forms as kbf
from telegram_io.telegram_menu.menu import get_user_functions_menu, profile_change_commands, get_inline_kb_registration

from telegram_io.dtos.profite import ProfileDto

admin_api = AdminApi()


async def process_start_command(msg: types.Message):
    """
    This handler will be called when user sends `/start`command
    """
    user = await admin_api.get_user_by_external_id(str(msg.from_user.id))
    if not user:
        await msg.reply(get_welcome_message(), reply_markup=kb.get_inline_kb_registration())
    else:
        await msg.reply(
            get_welcome_back_message_for_user(user),
            reply_markup=get_user_functions_menu(),
        )


async def process_callback_kb1btn1(callback_query: types.CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback_query.id)
    await kbf.RegisterForm.start.set()
    await bot.send_message(
        callback_query.from_user.id,
        get_agree_registration_message(),
        reply_markup=kb.reply_kb_phone_number,
    )


async def process_sign_up(message: types.Message, state: FSMContext):
    await kbf.RegisterForm.next()
    first_name = message.from_user.first_name
    await state.update_data(first_name=first_name)
    await kbf.RegisterForm.next()
    last_name = message.from_user.last_name
    await state.update_data(last_name=last_name)
    await kbf.RegisterForm.next()
    phone_number = normalize_phone_number(message.contact.phone_number)
    await state.update_data(phone=phone_number)
    await kbf.RegisterForm.next()
    country_name = get_country_by_phone(phone_number)
    await state.update_data(country=country_name)
    await kbf.RegisterForm.next()
    language = message.from_user.language_code
    await state.update_data(language=language)
    await kbf.RegisterForm.next()
    # for currency in moneyed.CURRENCIES:
    #     c = moneyed.CURRENCIES.get(currency)
    #     if country_name.upper() in c.countries:
    #         main_currency = currency
    #         break
    main_currency = "USD" #TODO
    await state.update_data(balance=main_currency)
    await kbf.RegisterForm.next()
    await message.answer(
        f"Full name: {message.from_user.last_name + ' ' + message.from_user.first_name}\n"
        f"phone number: {phone_number}\n"
        f"Country: {country_name}\n"
        f"Language: {language}\n"
        f"currency: {main_currency}\n"
        "Do you want to change some information?",
        reply_markup=kb.get_change_profile_menu(),
    )


async def process_callback_submit_profile_info(
    callback_query: types.CallbackQuery,
    callback_data: dict,
    bot: Bot,
    state: FSMContext,
):
    await bot.answer_callback_query(callback_query.id)
    profile_data = await state.storage.get_data(
        chat=callback_query.message.chat.id, user=callback_query.from_user.id
    )
    external_id = str(callback_query.from_user.id)

    is_user_exists = await admin_api.is_user_exists(external_id)
    if not is_user_exists:
        data = {
            "username": profile_data["phone"],
            "first_name": profile_data["first_name"],
            "last_name": profile_data["last_name"],
            "phone": profile_data["phone"],
            "country": profile_data["country"],
            "language": profile_data["language"],
            "balance": profile_data["balance"],
            "external_id": external_id,
        }
        profile_dto = ProfileDto(**data)
        await admin_api.create_new_user(profile_dto)
    else:
        profile_dto = admin_api.get_user_by_external_id(external_id)

    await state.finish()
    if profile_dto.id:
        message = "You have successfully registered"
        reply_markup = get_user_functions_menu()
    else:
        message = "Something went wrong. Please try again or contact to support!"
        reply_markup = get_inline_kb_registration()

    await bot.send_message(
        callback_query.message.chat.id, message, reply_markup=reply_markup
    )


async def define_change_field_profile_information(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    callback_data: dict,
    bot: Bot,
):
    class A:
        verbose_name = "str"
    await bot.answer_callback_query(callback_query.id)
    field_to_change = profile_change_commands.get(callback_query.data)
    field = A() #Profile._meta.get_field(field_to_change) #TODO
    message = "Enter your {}".format(field.verbose_name)
    state = State()
    for el in kbf.RegisterForm.all_states:
        if el._state == field_to_change:
            state = el
            break
    await state.set()
    await bot.send_message(callback_query.message.chat.id, message)


async def change_field_profile(message: types.Message, state: FSMContext):
    st = await state.get_state()
    validated = profile_validate_field(st.split(":")[1], message.text)
    if not validated:
        await message.bot.send_message(
            message.chat.id, "Wrong data,\nPlease enter valid data"
        )
        return
    await state.update_data({st.split(":")[1]: message.text})
    profile_data = await state.storage.get_data(
        chat=message.chat.id, user=message.from_user.id
    )
    await message.answer(
        f"Your Full name: {profile_data}\n"
        # f"Your phone number: {profile_data['phone']}\n" TODO not working RPW-7
        # f"Your country: {profile_data['country']}\n"
        # f"Your language: {profile_data['language']}\n"
        # f"Your currency: {profile_data['balance']}"
    )
    await message.answer(
        "Do you want to change some information?",
        reply_markup=kb.get_change_profile_menu(),
    )
    await kbf.RegisterForm.submit.set()


def register_handlers_registration(dp: Dispatcher, bot: Bot):
    dp.register_message_handler(process_start_command, commands="start")
    dp.register_message_handler(
        process_sign_up,
        content_types=types.ContentTypes.CONTACT,
        state=kbf.RegisterForm.start,
    )
    dp.register_message_handler(
        change_field_profile,
        state=[
            kbf.RegisterForm.first_name,
            kbf.RegisterForm.last_name,
            kbf.RegisterForm.phone,
            kbf.RegisterForm.country,
            kbf.RegisterForm.language,
            kbf.RegisterForm.balance,
        ],
    )

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("registration"))
    async def process_callback_kb1btn1_f(
        callback_query: types.CallbackQuery, bot: Bot = bot
    ):
        await process_callback_kb1btn1(callback_query=callback_query, bot=bot)

    @dp.callback_query_handler(
        lambda c: c.data and c.data.startswith(tuple(profile_change_commands.keys())),
        state="*",
    )
    async def define_change_field_profile_information_inline(
        callback_query: types.CallbackQuery,
        state: FSMContext,
        callback_data=None,
        bot: Bot = bot,
    ):
        if callback_data is None:
            callback_data = {}
        await define_change_field_profile_information(
            callback_query=callback_query,
            callback_data=callback_data,
            bot=bot,
            state=state,
        )

    @dp.callback_query_handler(
        lambda c: c.data and c.data.startswith("submit_profile_info"),
        state=kbf.RegisterForm.submit,
    )
    async def process_callback_submit_profile_info_f(
        callback_query: types.CallbackQuery, state: FSMContext, callback_data=None
    ):
        if not callback_data:
            callback_data = {}
        await process_callback_submit_profile_info(
            callback_query=callback_query,
            callback_data=callback_data,
            bot=bot,
            state=state,
        )
