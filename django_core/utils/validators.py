from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import ugettext as _


def is_valid_email(value):
    """Checks to see if the value is a valid email. Returns True if the email
    is valid. Otherwise, False.
    """
    try:
        validate_email(value)
        return True
    except ValidationError:
        return False


def validate_password_strength(value):
    """Validates that a password is as least 7 characters long and has at least
    1 digit and 1 letter.
    """
    min_length = 7

    if len(value) < min_length:
        raise ValidationError(_('Password must be at least {0} characters '
                                'long.').format(min_length))

    # check for digit
    if not any(char.isdigit() for char in value):
        raise ValidationError(_('Password must container at least 1 digit.'))

    # check for letter
    if not any(char.isalpha() for char in value):
        raise ValidationError(_('Password must container at least 1 letter.'))
