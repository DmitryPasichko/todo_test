import re
from pydantic import BaseModel, validator, ValidationError


class ProfileDto(BaseModel):
    id: int = 0
    username: str
    first_name: str
    last_name: str
    phone: str
    country: str = "Ukraine"
    language: str = "en"
    balance: str | None = 'USD'
    external_id: str
    email: str = "defualt@yopmail.com"


    @validator('phone')
    def phone_validation(cls, value: str) -> None:
        if not value:
            raise ValidationError('Phone should be set')
        if not re.fullmatch(r"\+38\d{10}", value):
            raise ValidationError('Phone is not acceptable. Use following format: +380111111111')
        return value

    @validator('email')
    def email_validation(cls, value: str) -> None:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if value and not re.fullmatch(regex, value):
            raise ValidationError('Email is not acceptable.')
        return value

    def get_profile_info(self) -> str:
        return (
            "Your Account data is:\nFirst name: {}\nLast name: {}\nPhone number: {}\nCountry: {}"
        ).format(
            self.first_name,
            self.last_name,
            self.phone,
            self.country,
        )

    def get_current_balance_message(self) -> str:
        return "Your current balance: {}".format(100)
