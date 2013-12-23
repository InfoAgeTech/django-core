# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.context import RequestContext


# TODO: This will soon be delete! DO NOT USE!
def html(template):
    """Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

    * template: template name to use

    :see: http://djangosnippets.org/snippets/821/

    """
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer


def turn_emails_off(view_func):
    """Turns emails off so no emails will be sent."""

    # Dummy email backend so no emails are sent.
    EMAIL_BACKEND_DUMMY = 'django.core.mail.backends.dummy.EmailBackend'

    def decorated(request, *args, **kwargs):
        orig_email_backend = settings.EMAIL_BACKEND
        settings.EMAIL_BACKEND = EMAIL_BACKEND_DUMMY

        response = view_func(request, *args, **kwargs)
        settings.EMAIL_BACKEND = orig_email_backend
        return response

    return decorated
