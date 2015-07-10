from __future__ import unicode_literals

from django.test.testcases import TestCase
from django_core.utils.random_utils import random_alphanum


class RandomUtilsTestCase(TestCase):
    """Test case for random utils."""

    def test_len_random_utils(self):
        """Test len of random utils string."""
        self.assertEqual(len(random_alphanum(15)), 15)

    def test_len_random_utils_high_length(self):
        """Test high random utils length."""
        self.assertEqual(len(random_alphanum(75)), 75)

    def test_random_utils_lower_only(self):
        """Test len of random utils for lower only characters."""
        random_val = random_alphanum(35, lower_only=True)
        self.assertEqual(len(random_val), 35)

        for c in random_val:
            if not c.isdigit() and not c.islower():
                self.fail('Random value has an upper case character: '
                          '{0}'.format(random_val))
