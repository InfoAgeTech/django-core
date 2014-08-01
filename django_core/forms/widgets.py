from __future__ import unicode_literals

from datetime import date
from datetime import datetime

from django.forms.widgets import DateInput
from django.forms.widgets import DateTimeInput
from django.forms.widgets import MultiWidget
from django.forms.widgets import TextInput
from django.utils.six import string_types


class ExtendedMultiWidget(MultiWidget):
    """Wrapper around the MultiWidget that allow for putting a custom css class
    around multiple widgets.
    """

    def __init__(self, widget_css_class=None, **kwargs):
        """
        :param widget_css_class: the string css class(es) to put around the
            entire widget.
        """
        self.widget_css_class = widget_css_class
        super(ExtendedMultiWidget, self).__init__(**kwargs)

    def format_output(self, *args, **kwargs):
        output = super(ExtendedMultiWidget, self).format_output(*args,
                                                                **kwargs)
        return '<div class="{0}">{1}</div>'.format(
            self.widget_css_class,
            output
        )


class Html5DateInput(DateInput):
    """Renders an HTML5 date widget."""
    input_type = 'date'

    def __init__(self, date_format='%Y-%m-%d', *args, **kwargs):
        super(Html5DateInput, self).__init__(*args, **kwargs)
        self.date_format = date_format

    def _format_value(self, value):
        value = super(Html5DateInput, self)._format_value(value)

        if self.date_format and isinstance(value, (date, datetime)):
            return value.strftime(self.date_format)

        return value


class Html5DateTimeInput(DateTimeInput):
    """Renders an HTML5 datetime widget."""
    input_type = 'datetime'

    def __init__(self, date_format='%Y-%m-%d %H:%M:%S', *args, **kwargs):
        super(Html5DateTimeInput, self).__init__(date_format=date_format,
                                                 *args,
                                                 **kwargs)


class ReadonlyWidget(TextInput):
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


class CommaSeparatedListWidget(TextInput):
    """Widget for rendering a comma separated list using a text field."""

    def __init__(self, *args, **kwargs):
        super(CommaSeparatedListWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if isinstance(value, (list, tuple)):
            # It's a list, join the values for display
            value = ', '.join(map(str, value))

        return super(CommaSeparatedListWidget, self).render(name=name,
                                                            value=value,
                                                            attrs=attrs)

    def value_from_datadict(self, data, files, name, **kwargs):
        value = super(CommaSeparatedListWidget,
                      self).value_from_datadict(data=data, files=files,
                                                name=name, **kwargs)

        if value and isinstance(value, string_types):
            return [item.strip() for item in value.split(',') if item.strip()]

        return value
