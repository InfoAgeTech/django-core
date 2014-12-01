from django.test.testcases import TestCase
from django_core.utils.urls import replace_url_query_values


class UrlUtilsTestCase(TestCase):
    """Test case for url utils."""

    def test_replace_url_query_values(self):
        """Test replacing querysting values in a url."""
        url = 'http://helloworld.com/some/path?test=5'
        replace_vals = {'test': 10}
        new_url = replace_url_query_values(url=url, replace_vals=replace_vals)
        self.assertEqual(new_url, 'http://helloworld.com/some/path?test=10')
