from django.core.exceptions import ValidationError
from django.test.testcases import TestCase
from django_core.forms.fields import CommaSeparatedIntegerListField
from django_core.forms.fields import CommaSeparatedListField


class FormFieldsTestCase(TestCase):
    """Test case for form fields."""

    def test_comma_separated_list_field_valid_clean(self):
        """Tests that the comma separated list field correctly cleans the
        value.
        """
        words = ['hello', 'world', 'test']
        words_string = '{0}, {1},     {2}'.format(*words)
        field = CommaSeparatedListField()
        cleaned_value = field.to_python(words_string)
        self.assertEqual(words, cleaned_value)

    def test_comma_separated_list_field_validate(self):
        """Tests that the comma separated list field correctly validates the
        cleaned value.
        """
        words = ['hello', 'world', 'test']
        field = CommaSeparatedListField()
        self.assertIsNone(field.validate(words))

    def test_comma_separated_list_field_invalid_max_length(self):
        """Tests that the comma separated list field correctly validates a list
        that's too long.
        """
        words = ['hello', 'world', 'test']
        field = CommaSeparatedListField(max_list_length=2)

        with self.assertRaises(ValidationError):
            self.assertIsNone(field.validate(words))

    def test_comma_separated_integer_list_field_valid(self):
        """Test the CommaSeparatedIntegerListField correctly cleans a list of
        integers.
        """
        int_list = [1, 4, 2, 5]
        ints_string = '{0},{1}, {2}  ,   {3}'.format(*int_list)
        field = CommaSeparatedIntegerListField()
        self.assertEqual(int_list, field.to_python(ints_string))

    def test_comma_separated_integer_list_field_invalid(self):
        """Test the CommaSeparatedIntegerListField correctly throws an error
        when a list of non-integers is passed.
        """
        non_ints = '1, 4, hello, 5'
        field = CommaSeparatedIntegerListField()

        with self.assertRaises(ValidationError):
            field.clean(non_ints)
