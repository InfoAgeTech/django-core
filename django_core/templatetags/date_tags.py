from datetime import datetime

from django.template import Library


register = Library()


@register.simple_tag
def utcnow(**kwargs):
    """Template tag for getting the current datetime utcnow."""
    return datetime.utcnow()


@register.simple_tag
def utcnow_timestamp(**kwargs):
    """Template tag for getting the current datetime utcnow timestamp."""
    return datetime.utcnow().timestamp()
