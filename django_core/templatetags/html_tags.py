from django import template
from django.utils.html import linebreaks
from django.utils.safestring import mark_safe
from django.utils.six import string_types


register = template.Library()


@register.filter
def linebreaks_safe(value):
    """
    Adds linebreaks only for text that has a newline character.
    """
    if isinstance(value, string_types) and '\n' in value:
        return mark_safe(linebreaks(value))

    return value
