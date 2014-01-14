# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.forms.fields import CharField


class CharFieldStripped(CharField):
    """Wrapper around CharField that strips whitespace from the CharField when
    validating so .strip() doesn't have to be called every time you validate
    the field's data.
    """

    def clean(self, value):
        if value:
            value = value.strip()

        return super(CharFieldStripped, self).clean(value)


class CommaSeparatedListField(CharFieldStripped):
    """Form field that takes a string and converts into a list of strings."""

    def clean(self, value):
        value = super(CharFieldStripped, self).clean(value)
        return [item.strip() for item in value.split(',') if item.strip()]


class CommaSeparatedIntegerListField(CommaSeparatedListField):
    """Comma Separated Integer list field."""
    # TODO: this should honor:
    #    max_value (each item in the list can't be > this value)
    #    min_value (each item in the list can't be < this value)
    #    max_length (could be the number of items in the list)

    def clean(self, value):
        val = super(CommaSeparatedIntegerListField, self).clean(value)

        if isinstance(value, (list, tuple)):
            # Ensure all values are integers
            try:
                val = [int(item) for item in val]
            except:
                raise ValidationError('All values in list must be whole '
                                      'numbers.')
        return val
