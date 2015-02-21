from django.test.testcases import TestCase
from django_core.utils.urls import get_query_values_from_url
from django_core.utils.urls import replace_url_query_values
from django_core.utils.urls import is_legit_next_url


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

    def test_is_legit_next_url_fully_qualified_domain(self):
        """Test for legit urls coming from a fully qualified domain."""
        domain = 'example.com'
        path = '/some/path?test=5'
        url_no_scheme = '//{0}{1}'.format(domain, path)
        url = 'http:{0}'.format(url_no_scheme)

        with self.settings(SITE_DOMAIN=domain):
            self.assertTrue(is_legit_next_url(url))
            self.assertTrue(is_legit_next_url(url_no_scheme))
            self.assertTrue(is_legit_next_url(path))

    def test_is_legit_next_url_fully_qualified_domain_with_subdomain(self):
        """Test for legit urls coming from a fully qualified domain with a
        subdomain.
        """
        domain = 'example.com'
        url_no_scheme = '//blog.{0}/some/path?test=5'.format(domain)
        url = 'http:{0}'.format(url_no_scheme)

        with self.settings(SITE_DOMAIN=domain):
            self.assertTrue(is_legit_next_url(url))
            self.assertTrue(is_legit_next_url(url_no_scheme))

    def test_is_legit_next_url_fully_qualified_domain_with_port(self):
        """Test for legit urls coming from a fully qualified domain with a port
        number.
        """
        domain = 'example.com'
        url_no_scheme = '//{0}:8010/some/path?test=5'.format(domain)
        url = 'http:{0}'.format(url_no_scheme)

        with self.settings(SITE_DOMAIN=domain):
            self.assertTrue(is_legit_next_url(url))
            self.assertTrue(is_legit_next_url(url_no_scheme))

    def test_is_legit_next_url_fully_qualified_domain_not_legit(self):
        """Test for ensuring non known domains don't pass validation."""
        domain = 'example.com'
        url_no_scheme = '//badapple.com/some/path?test=5'.format(domain)
        url = 'http:{0}'.format(url_no_scheme)

        with self.settings(SITE_DOMAIN=domain):
            self.assertFalse(is_legit_next_url(url))
            self.assertFalse(is_legit_next_url(url_no_scheme))
