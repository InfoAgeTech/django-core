# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import redirect


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
