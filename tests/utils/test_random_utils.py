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
