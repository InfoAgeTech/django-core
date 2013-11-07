# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def is_valid_email(value):
    """Checks to see if the value is a valid email. Returns True if the email
    is valid. Otherwise, False.
    """
    try:
        validate_email(value)
        return True
    except ValidationError:
        return False