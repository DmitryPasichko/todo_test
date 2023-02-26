import logging
# import moneyed
import itertools
from django_countries.data import COUNTRIES

from telegram_io.languages import LANGUAGES
from telegram_io.utils.phone import normalize_phone_number

logger = logging.Logger("phone utils")


def profile_validate_field(field_name: str, value: str):
    if field_name in ["first_name", "last_name"]:
        if len(value) < 2 or has_numbers(value):
            return False
    if field_name == "phone_number":
        if not validate_phone_international(value):
            return False
    if field_name == "country":
        if value.title() not in COUNTRIES.values():
            return False
    if field_name == "language":
        if value.lower() not in itertools.chain(*LANGUAGES):
            return False
    if field_name == "balance":
        # if value not in moneyed.CURRENCIES:
            return False
    return True


def has_numbers(string):
    return any(char.isdigit() for char in string)


def validate_phone_international(phone: str):
    try:
        normalize_phone_number(phone)
    except Exception as e:
        logger.error(f"phone: {phone} hasn't been validated {e}")
        return False
    return True
