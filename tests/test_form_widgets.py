from django.test.testcases import TestCase
from django_core.forms.widgets import CommaSeparatedListWidget


class CommaSeparatedListWidgetTestCase(TestCase):

    def test_widget_value_from_datadict(self):
        field_name = 'some_field'
        data = {field_name: '1,4, 5 , hello'}
        widget = CommaSeparatedListWidget()
        value = widget.value_from_datadict(data=data, files={}, name=field_name)
        self.assertEqual(value, ['1', '4', '5', 'hello'])

    def test_widget_value_from_datadict_ints(self):
        field_name = 'some_field'
        data = {field_name: '1,4,5'}
        widget = CommaSeparatedListWidget()
        value = widget.value_from_datadict(data=data, files={}, name=field_name)
        self.assertEqual(value, ['1', '4', '5'])
