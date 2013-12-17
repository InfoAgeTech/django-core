# -*- coding: utf-8 -*-

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class CsrfExemptViewMixin(object):
    """Mixin for the csrf_exempt decorator."""

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CsrfExemptViewMixin, self).dispatch(*args, **kwargs)
