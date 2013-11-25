# -*- coding: utf-8 -*-
"""
 This snippet modified from djangosnippets.com:
  http://www.djangosnippets.org/snippets/1799/
"""

from django.core.urlresolvers import get_callable
from django.http import HttpResponseNotAllowed


class Dispatcher(object):
    """Calls a view by request.method value.

    To use this dispatcher write your urls.py like this::

        urlpatterns = pattern('',
            url(r'^foo/$', dispatch(head='views.foo_head',
                                    get='views.foo_page',
                                    delete='views.foo_delete',
                                    post='views.foo_add',)),
        )

    If request.method is equal to head, the foo_head view will be called; if it
    is "get", foo_page will be called; et cetera.

    If the method specified in request.method is not one handled by
    dispatch(..), HttpResponseNotAllowed is returned.

    """

    @property
    def __name__(self):
        """Returns a name to distinguish dispatch objects.

        In newer versions of DjangoDebugToolbar and Django, there is an
        expectation that wrapped view objects have a usable __name__ attribute.

        Since Dispatcher is a multiplexing decorator (i.e. a single Dispatcher
        wraps multiple functions), it cannot simply retrieve these values using
        functools.wraps as with other decorators. As such, this property
        generates a name that describes this as a dispatcher and contains the
        mapping of HTTP methods to views.

        """

        return str(self)

    def __init__(self, **methods):
        self.__method_map = dict((method.lower(), handler) for method, handler
                                 in methods.iteritems())

    def __getitem__(self, key):
        """Gets the view function for the lowercase version of the method key.

        Must return None if no such method exists.

        """

        return self.__method_map.get(key.lower())

    def __getattr__(self, attr):
        """Retrieve attributes from the dictionary.

        This allows access to things like .keys() and .values().

        """

        return getattr(self.__method_map, attr)

    def __str__(self):
        """Generates a string representation of the dispatcher object that
        contains the mapping of HTTP methods to views to help distinguish
        dispatcher objects in view calls.

        """

        return 'Dispatcher: {0}'.format(self.__method_map)

    def __call__(self, request, *args, **kwargs):
        handler = self.__method_map.get(request.method.lower())

        if isinstance(handler, tuple):
            handler, kw = handler
            kwargs.update(kw)

        handler = handler and get_callable(handler)

        return (handler(request, *args, **kwargs) if handler else
                HttpResponseNotAllowed(method.upper() for method in
                                       self.keys()))

dispatch = Dispatcher
