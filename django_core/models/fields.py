# -*- coding: utf-8 -*-
import ast
import json

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _


class ListField(models.TextField):
    """Model field for python lists."""
    __metaclass__ = models.SubfieldBase

    description = "Stores a python list"

    default_error_messages = {
        'invalid_list': _("'%(value)s' value must be a list type."),
        'invalid_choice': _("'%(value)s' is not a valid choice.")
    }

    def to_python(self, value):
        if value == None:
            return value

        if not value:
            return []

        if isinstance(value, list):
            if len(value) == 0 or not self.choices:
                return value

            # Validate choices
            valid_choices = tuple(choice[0] for choice in self.choices)

            for item in value:
                if item not in valid_choices:
                    raise ValidationError(
                        self.error_messages['invalid_choice'],
                        code='invalid_choice',
                        params={'value': item}
                    )

            return value

        try:
            return ast.literal_eval(value)
        except ValueError as e:
            raise ValidationError(
                self.error_messages['invalid_list'],
                code='invalid_list',
                params={'value': value}
            )

    def get_prep_value(self, value):
        if value is None:
            return value

        if not isinstance(value, list):
            raise ValidationError(
                self.error_messages['invalid_list'],
                code='invalid_list',
                params={'value': value}
            )

        return super(ListField, self).get_prep_value(value)


class IntegerListField(ListField):
    """Wrapper around ListField ensuring all values are integers."""
    __metaclass__ = models.SubfieldBase

    default_error_messages = {
        'invalid_integers': _('All values in list "%(value)s" must be of '
                              'integer types.'),
        'invalid_out_of_range_min': _('"%(value)s" out of range. Must be '
                                      'greater than or equal to %(min)s'),
        'invalid_out_of_range_max': _('"%(value)s" out of range. Must be '
                                      'less than or equal to %(max)s')
    }

    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        """
        :param min_value: the minimum value that can be in the list
        :param max_value: the maximum value that can be in the list
        """
        self.min_value = min_value
        self.max_value = max_value
        super(IntegerListField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):

        if isinstance(value, list):

            # Validate that all items in the list are integers.
            for item in value:
                if not isinstance(item, int):
                    raise ValidationError(
                        self.error_messages['invalid_integers'],
                        code='invalid_integers',
                        params={'value': value}
                    )

                if self.min_value != None and item < self.min_value:
                    raise ValidationError(
                        self.error_messages['invalid_out_of_range_min'],
                        code='invalid_out_of_range_min',
                        params={'value': value, 'min': self.min_value}
                    )

                if self.max_value != None and item > self.max_value:
                    raise ValidationError(
                        self.error_messages['invalid_out_of_range_max'],
                        code='invalid_out_of_range_max',
                        params={'value': value, 'max': self.max_value}
                    )

        return super(IntegerListField, self).get_prep_value(value)


class JSONField(models.TextField):
    """Simple JSON field that stores python structures as JSON strings
    on database.

    Borrowed from django-social-auth :):

    https://github.com/omab/django-social-auth/blob/master/social_auth/fields.py

    """
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """
        Convert the input JSON value into python structures, raises
        django.core.exceptions.ValidationError if the data can't be converted.
        """
        if self.blank and not value:
            return None
        if isinstance(value, basestring):
            try:
                return json.loads(value)
            except Exception, e:
                raise ValidationError(str(e))
        else:
            return value

    def validate(self, value, model_instance):
        """Check value is a valid JSON string, raise ValidationError on
        error."""
        if isinstance(value, basestring):
            super(JSONField, self).validate(value, model_instance)
            try:
                json.loads(value)
            except Exception, e:
                raise ValidationError(str(e))

    def get_prep_value(self, value):
        """Convert value to JSON string before save"""
        try:
            return json.dumps(value)
        except Exception, e:
            raise ValidationError(str(e))

    def value_to_string(self, obj):
        """Return value from object converted to string properly"""
        return smart_unicode(self.get_prep_value(self._get_val_from_obj(obj)))
