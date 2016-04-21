from django import template
from django.template.defaultfilters import linebreaks_filter
from django.utils.six import string_types


# from django.utils.html import linebreaks
register = template.Library()


@register.filter
def linebreaks_safe(value, autoescape=True):
    """
    Adds linebreaks only for text that has a newline character.
    """
    if isinstance(value, string_types) and '\n' in value:
        return linebreaks_filter(value, autoescape=autoescape)

    return value
