# -*- coding: utf=8 -*-
from django import forms


class ReadonlyWidget(forms.TextInput):
    """This renders a readonly field that can also override the default display
    value.
    """
    def render(self, name, value, attrs=None):
        if 'readonly' not in self.attrs:
            # Make sure the field renders as readonly
            self.attrs['readonly'] = 'readonly'

        if 'value' in self.attrs:
            # Override the display value
            value = self.attrs.get('value')

        return super(ReadonlyWidget, self).render(name, value, attrs=attrs)
