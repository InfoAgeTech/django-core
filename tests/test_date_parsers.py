from datetime import date
from datetime import datetime
from unittest.case import TestCase

from django_core.utils.date_parsers import hex_timestamp_to_datetime
from django_core.utils.date_parsers import parse_date


class DateParsersTestCase(TestCase):
    """Test case for date parsers."""

    def test_hex_timestamp_to_datetime(self):
        """Test the conversion of a hex timestamp to a datetime object."""
        dt = datetime(2015, 6, 25, 8, 34, 1)
        self.assertEqual(hex_timestamp_to_datetime('558BBCF9'), dt)
        self.assertEqual(hex_timestamp_to_datetime('0x558BBCF9'), dt)
        self.assertEqual(datetime.fromtimestamp(0x558BBCF9), dt)

    def test_parse_date(self):
        """Test parsing dates."""
        dt = date(2015, 12, 31)
        self.assertEqual(parse_date('2015-12-31'), dt)
        self.assertEqual(parse_date('12/31/2015'), dt)