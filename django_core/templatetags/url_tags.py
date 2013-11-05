# -*- coding: utf-8 -*-
from django.template import Library
from django.utils.html import escape

register = Library()


@register.filter
def get_absolute_url_link(obj, text=None):
    """Gets the absolute url html link for the object.

    Usage:

    {{ obj|get_absolute_url_link:"Some Text" }}

    Would return:

    u'<a href="{{ THE OBJ ABSOLUTE URL }}">{{ TEXT THAT WAS PASSED IN }}</a>'
    """

    if hasattr(obj, 'get_absolute_url_link'):
        return obj.get_absolute_url_link(text=text)

    if text:
        text = escape(text)

    absolute_url = obj.get_absolute_url()
    return u'<a href="{0}">{1}</a>'.format(absolute_url,
                                           text or absolute_url)


@register.filter
def get_edit_url_link(obj, text=None):
    """Gets the absolute url html link for the object.

    Usage:

    {{ obj|get_edit_url_link:"Some Text" }}

    Would return:

    u'<a href="{{ THE OBJ EDIT URL }}">{{ TEXT THAT WAS PASSED IN }}</a>'
    """

    if hasattr(obj, 'get_absolute_url_link'):
        return obj.get_edit_url_link(text=text)

    if text:
        text = escape(text)

    edit_url = obj.get_edit_url()
    return u'<a href="{0}">{1}</a>'.format(edit_url,
                                           text or edit_url)


@register.filter
def get_delete_url_link(obj, text=None):
    """Gets the absolute url html link for the object.
    """

    if hasattr(obj, 'get_absolute_url_link'):
        return obj.get_delete_url_link(text=text)

    if text:
        text = escape(text)

    delete_url = obj.get_delete_url()
    return u'<a href="{0}">{1}</a>'.format(delete_url,
                                           text or delete_url)
