from django.test.testcases import TestCase
from django_core.forms.widgets import CommaSeparatedListWidget
from django_core.forms.widgets import MultipleDecimalInputWidget


class CommaSeparatedListWidgetTestCase(TestCase):

    def test_widget_value_from_datadict(self):
        field_name = 'some_field'
        data = {field_name: '1,4, 5 , hello'}
        widget = CommaSeparatedListWidget()
        value = widget.value_from_datadict(data=data, files={},
                                           name=field_name)
        self.assertEqual(value, ['1', '4', '5', 'hello'])

    def test_widget_value_from_datadict_ints(self):
        field_name = 'some_field'
        data = {field_name: '1,4,5'}
        widget = CommaSeparatedListWidget()
        value = widget.value_from_datadict(data=data, files={},
                                           name=field_name)
        self.assertEqual(value, ['1', '4', '5'])


class MultipleDecimalInputWidgetTestCase(TestCase):
    """Test case for the multiple decimal input widget."""

    def test_widget_value_from_data_dict(self):
        field_name = 'some_field'
        data = {
            '{0}_0'.format(field_name): '3',
            '{0}_1'.format(field_name): '2',
            '{0}_2'.format(field_name): '1'
        }
        widget = MultipleDecimalInputWidget(num_inputs=3)
        value = widget.value_from_datadict(data=data, files={},
                                           name=field_name)
        self.assertEqual(value, ['3', '2', '1'])

    def test_widget_decompress(self):
        val_1 = '5'
        val_2 = '4'
        val_3 = '1'
        val_4 = '0'
        widget = MultipleDecimalInputWidget()
        value = '{0} {1} {2} {3}'.format(val_1, val_2, val_3, val_4)

        decompressed_value = widget.decompress(value)
        self.assertEqual(decompressed_value[0], val_1)
        self.assertEqual(decompressed_value[1], val_2)
        self.assertEqual(decompressed_value[2], val_3)
        self.assertEqual(decompressed_value[3], val_4)
