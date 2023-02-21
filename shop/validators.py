######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from django.core.exceptions import ValidationError


def validate_line_quantity(value):
    if value <= 0:
        raise ValidationError(
            f"Quantity was set incorrect. Value should be greater than 0"
        )
