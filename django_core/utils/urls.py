from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import redirect
from django.utils.http import urlencode

try:
    # python 3
    from urllib.parse import urlparse
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import urlparse
    from urlparse import parse_qsl


def is_legit_next_url(next_url):
    if not next_url or next_url.startswith('//'):
        # Either no next or some //evil.com hackery, denied!
        return False

    # Make sure it's a resource on this site...
    return next_url.startswith('/') or next_url.startswith(settings.SITE_ROOT_URI)


def safe_redirect(next_url, default=None):
    """Makes sure it's a legit site to redirect to.

    :param default: this is the default url or named url to redirect to in the
        event where next_url is not legit.

    """
    if is_legit_next_url(next_url):
        return redirect(next_url)

    if default:
        return redirect(default)

    return redirect('/')


def build_url(url, querystring_params=None):
    """Builds a url string with properly encoded queryparams.
    
    :params url: the primary url with no querystring params.  I.E. 
        http://somesite.com/path/to/page
    :param querystring_params: dict of querystring key value pairs.    
    """
    if not querystring_params:
        return url

    return '{0}?{1}'.format(url, urlencode(querystring_params))


def replace_url_query_values(url, replace_vals):
    """Replace querystring values in a url string.
    
    >>> url = 'http://helloworld.com/some/path?test=5'
    >>> replace_vals = {'test': 10}
    >>> replace_url_query_values(url=url, replace_vals=replace_vals)
    'http://helloworld.com/some/path?test=10'
    """
    if '?' not in url:
        return url

    parsed_url = urlparse(url)
    query = dict(parse_qsl(parsed_url.query))
    query.update(replace_vals)
    return '{0}?{1}'.format(url.split('?')[0], urlencode(query))
