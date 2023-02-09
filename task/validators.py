from django.core.exceptions import ValidationError
from functools import wraps


def validate_level(max_level):
    """
    Check that level must be less than 2
    :param max_level:
    :return:
    """
    @wraps(validate_level)
    def validator(value):
        if value > max_level:
            raise ValidationError("Impossible to add new comment")

    return validator
