import phonenumbers
import logging

from phonenumbers import geocoder

logger = logging.Logger("phone utils")


def normalize_phone_number(phone: str) -> str:
    if "+" not in phone:
        phone = "+" + phone
        phone = phonenumbers.format_number(
            phonenumbers.parse(phone), phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
    return phone.replace(" ", "")


def get_country_by_phone(phone: str) -> str:
    try:
        country = geocoder.description_for_number(phonenumbers.parse(phone), "en")
    except Exception as e:
        logger.error(f"Country for phone: {phone} hasn't got {e}")
    return country
