from django.test.testcases import TestCase
from django_core.utils.urls import get_query_values_from_url
from django_core.utils.urls import replace_url_query_values


class UrlUtilsTestCase(TestCase):
    """Test case for url utils."""

    def test_replace_url_query_values(self):
        """Test replacing querysting values in a url."""
        url = 'http://helloworld.com/some/path?test=5'
        replace_vals = {'test': 10}
        new_url = replace_url_query_values(url=url, replace_vals=replace_vals)
        self.assertEqual(new_url, 'http://helloworld.com/some/path?test=10')

    def test_get_query_values_from_url_single_key(self):
        """Test getting query values from a url."""
        url = 'http://helloworld.com/some/path?test=5&hello=world&john=doe'
        self.assertEqual("5", get_query_values_from_url(url=url, keys='test'))

    def test_get_query_values_from_url_single_key_list(self):
        """Test getting query values from a url."""
        url = 'http://helloworld.com/some/path?test=5&hello=world&john=doe'
        self.assertEqual(
            {'test': '5'},
            get_query_values_from_url(url=url, keys=['test'])
        )

    def test_get_query_values_from_url_multiple_key_list(self):
        """Test getting multiple query values from a url."""
        url = 'http://helloworld.com/some/path?test=5&hello=world&john=doe'
        self.assertEqual(
            {'test': '5', 'john': 'doe'},
            get_query_values_from_url(url=url, keys=['test', 'john'])
        )

    def test_get_query_values_from_url_multiple_key_list_key_not_present(self):
        """Test getting multiple query values from a url with key that doesn't 
        exist in the url.
        """
        url = 'http://helloworld.com/some/path?test=5&hello=world&john=doe'
        self.assertEqual(
            {'test': '5', 'john': 'doe', 'blah': None},
            get_query_values_from_url(url=url, keys=['test', 'john', 'blah'])
        )
