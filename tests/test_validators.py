from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.test.testcases import TestCase
from django_core.utils.validators import is_valid_email
from django_core.utils.validators import validate_password_strength
from django_core.utils.validators import is_valid_hex
from django_core.utils.validators import is_valid_color_name
from django_core.utils.validators import is_valid_color
from django_core.utils.validators import is_valid_rgb_color


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

    def test_is_valid_color(self):
        """Test the is_valid_color method returns correct boolean for valid
        colors.
        """
        self.assertTrue(is_valid_color('black'))
        self.assertTrue(is_valid_color('#aabb11'))
        self.assertTrue(is_valid_color('rgba(23,45,67, .5)'))
        self.assertFalse(is_valid_color('bl(ack'))

    def test_is_valid_hex(self):
        """Test the is_valid_hex method returns correct boolean for valid
        hex values.
        """
        self.assertTrue(is_valid_hex('#aabb11'))
        self.assertTrue(is_valid_hex('#000'))
        self.assertTrue(is_valid_hex('#aaa'))
        self.assertFalse(is_valid_hex('black'))
        self.assertFalse(is_valid_hex('bl(ack'))

    def test_is_valid_color_name(self):
        """Test the is_valid_color_name method returns correct boolean for
        valid color names.
        """
        self.assertTrue(is_valid_color_name('black'))
        self.assertTrue(is_valid_color_name('red'))
        self.assertFalse(is_valid_color_name('#aabb11'))
        self.assertFalse(is_valid_color_name('bl(ack'))

    def test_is_valid_rgb_color(self):
        """Test the is_valid_rgb_color method returns the correct boolean for
        valid rgb and rgba colors.
        """
        self.assertTrue(is_valid_rgb_color('rgb(12,23,5)'))
        self.assertTrue(is_valid_rgb_color('rgb(12, 223, 225)'))
        self.assertTrue(is_valid_rgb_color('rgba(12, 223, 225, 1)'))
        self.assertTrue(is_valid_rgb_color('rgba(12, 223, 225, 1.0)'))
        self.assertTrue(is_valid_rgb_color('rgba(12, 223, 225, 0)'))
        self.assertTrue(is_valid_rgb_color('rgba(12, 223, 225, .3)'))
        self.assertTrue(is_valid_rgb_color('rgba(12, 223, 225, .34521)'))

        # invalid cases
        self.assertFalse(is_valid_rgb_color('rgb(12, 223, 225, 0.5)'))
        self.assertFalse(is_valid_rgb_color('rgb(12, 223, 225, 5)'))
        self.assertFalse(is_valid_rgb_color('rgb(1234, 223, 225)'))
        self.assertFalse(is_valid_rgb_color('rgba(1234, 223, 225,.5)'))
        self.assertFalse(is_valid_rgb_color('rgba(1234, 223, 225,1.1)'))
