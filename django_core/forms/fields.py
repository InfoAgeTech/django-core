from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.forms.fields import DecimalField
from django.forms.fields import MultiValueField

from .widgets import MultipleDecimalInputWidget
from django.forms.fields import ChoiceField
from django_core.forms.widgets import ChoiceAndCharInputWidget


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


class MultipleDecimalField(MultiValueField):
    widget = MultipleDecimalInputWidget

    def __init__(self, num_inputs=2, *args, **kwargs):
        self.num_inputs = num_inputs
        fields = [DecimalField(required=False)
                  for i in range(num_inputs)]
        widget = self.widget(num_inputs=num_inputs)
        super(MultipleDecimalField, self).__init__(fields=fields,
                                                   widget=widget,
                                                   *args, **kwargs)

    def to_python(self, value):
        """Validates that the input can be converted to a list of decimals."""
        if not value:
            return None

        if isinstance(value, list):
            for index, position_val in enumerate(value):
                val = super(MultipleDecimalField, self).to_python(position_val)
                value[index] = val

        return value


class ChoiceAndCharField(MultiValueField):
    widget = ChoiceAndCharInputWidget

    def __init__(self, choices=None, widget_css_class='', *args, **kwargs):

        if 'widget' in kwargs:
            self.widget = kwargs.pop('widget')

        fields = (
            ChoiceField(choices=choices, required=False),
            CharField(required=False)
        )

        widget_kwargs = {
            'choices': choices
        }

        if widget_css_class:
            css_class = 'choice-and-char-widget {0}'.format(widget_css_class)
            widget_kwargs['widget_css_class'] = css_class

        widget = self.widget(**widget_kwargs)
        super(ChoiceAndCharField, self).__init__(fields=fields,
                                                 widget=widget,
                                                 *args,
                                                 **kwargs)

    def compress(self, data_list):
        return data_list
