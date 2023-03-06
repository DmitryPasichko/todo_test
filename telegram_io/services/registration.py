# from RaccoonPayWebService.models.client_profile import Profile
# from djmoney.money import Money
from django_countries import Countries


async def get_or_register_user(
    first_name,
    last_name,
    phone,
    country,
    lang,
    currency,
    messenger_id,
    external_user_id,
):
    pass
    # profile = await Profile.objects.aget_or_create(
    #     phone_number=phone,
    #     country=get_country_by_name(country),
    #     defaults={
    #         "first_name": first_name,
    #         "last_name": last_name,
    #         "language": lang,
    #         "balance": Money(currency=currency),
    #     },
    # )[0]
    # profile.add_messenger_to_user(
    #     messenger_id=messenger_id, external_user_id=external_user_id
    # ) TODO RPW-8


def get_country_by_name(country_name):
    return Countries().by_name(country=country_name)


def get_welcome_back_message_for_user(user) -> str:
    return (
        "Welcome back to Gallant Clothes! Your Account data is:\nFirst name: {}\nLast name: {}\nPhone number: {}\nCountry: {}\nCurrency: {}"
    ).format(
        user.first_name,
        user.last_name,
        user.phone,
        user.country,
        user.balance,
    )


def get_welcome_message() -> str:
    return "Welcome to Gallant Clothes! Do you want to sign up?"


def get_agree_registration_message() -> str:
    return (
        "For sign up, please, share with us your contact data. "
        "By clicking “Accept & Share my Contact” button you accept and "
        "agree with “Privacy Policy”, “Terms & Conditions” and “Public Offer” statements"
    )


