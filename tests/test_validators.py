from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.test.testcases import TestCase
from django_core.utils.validators import is_valid_email
from django_core.utils.validators import validate_password_strength


class ValidatorsTestCase(TestCase):
    """TestCase for validators."""

    def test_is_valid_email(self):
        """Test for validating an email is valid."""
        self.assertTrue(is_valid_email('abc@example.com'))

    def test_is_invalid_email(self):
        """Test for validating an email is invalid."""
        self.assertFalse(is_valid_email('helloworld'))

    def test_password_strength_validator(self):
        """Test for successful password strength validation."""
        self.assertIsNone(validate_password_strength('abcd123'))

    def test_password_strength_validator_length_fail(self):
        """Test for length fail password strength validation."""
        with self.assertRaises(ValidationError):
            validate_password_strength('hi')

    def test_password_strength_validator_missing_digit(self):
        """Test for password strength missing digit."""
        with self.assertRaises(ValidationError):
            validate_password_strength('abcdefg')

    def test_password_strength_validator_missing_letter(self):
        """Test for password strength missing letter."""
        with self.assertRaises(ValidationError):
            validate_password_strength('1234567')
