from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.test import TestCase

from test_objects.models import TestIntegerListFieldModel
from test_objects.models import TestListFieldModel


class ListFieldTests(TestCase):
    """Test case for ListField."""

    def test_initialization(self):
        """Test for initializing the list fields."""
        list_field = ['hello', 'world', 5]
        list_field_not_required = ['again', 'testing', 10]

        x = TestListFieldModel(
            list_field=list_field,
            list_field_not_required=list_field_not_required
        )

        self.assertEqual(x.list_field, list_field)
        self.assertEqual(x.list_field_not_required, list_field_not_required)

    def test_list_field_db_retrieval(self):
        """Test to ensure value is correctly saved and retrieved from db."""
        list_field = ['hello', 'world', 5]
        list_field_not_reqired = ['again', 'testing', 10]

        obj = TestListFieldModel()
        obj.list_field = list_field
        obj.list_field_not_required = list_field_not_reqired
        obj.save()

        obj_db = TestListFieldModel.objects.get(id=obj.id)

        self.assertEqual(obj_db.list_field, list_field)
        self.assertEqual(obj_db.list_field_not_required,
                         list_field_not_reqired)

    def test_validation_error_non_list(self):
        """Test validation error occurs when trying to save a values that's not
        a list.
        """
        with self.assertRaises(ValidationError):
            x = TestListFieldModel(list_field='testing')
            x.save()

    def test_validation_error_non_list_required_field(self):
        """Test validation error occurs when trying to save a values that's not
        a list.
        """
        x = TestListFieldModel()
        x.save()

        self.assertEqual(x.list_field, [])
        self.assertIsNone(x.list_field_not_required)

    def test_choice_validation_success(self):
        """Test validating a ListField with choices."""
        x = TestListFieldModel()
        x.list_field_choices = ['HELLO', 'WORLD']
        x.save()

    def test_choice_validation_error(self):
        """Test validating a ListField with choices that throws a
        ValidationError for not having a valid choice."""
        x = TestListFieldModel()

        with self.assertRaises(ValidationError):
            x.list_field_choices = ['HELLO', 'NOT_A_VALID_CHOICE']


class IntegerListFieldTests(TestCase):
    """Test case for IntegerListField."""

    def test_initialization(self):
        """Test for initializing the list fields."""
        int_list_field = [1, 4, 2]
        int_list_field_not_required = [6, 3, 2]
        x = TestIntegerListFieldModel(
            int_list_field=int_list_field,
            int_list_field_not_required=int_list_field_not_required
        )

        self.assertEqual(x.int_list_field, int_list_field)
        self.assertEqual(x.int_list_field_not_required,
                         int_list_field_not_required)

    def test_db_retrieval(self):
        """Test to ensure value is correctly saved and retrieved from db."""
        int_list_field = [1, 4, 2]
        int_list_field_not_required = [6, 3, 2]

        obj = TestIntegerListFieldModel()
        obj.int_list_field = int_list_field
        obj.int_list_field_not_required = int_list_field_not_required
        obj.save()

        obj_db = TestIntegerListFieldModel.objects.get(id=obj.id)

        self.assertEqual(obj_db.int_list_field, int_list_field)
        self.assertEqual(obj_db.int_list_field_not_required,
                         int_list_field_not_required)

    def test_validation_error_non_int(self):
        """Test validation error occurs when trying to save a values that's not
        a list of integers.
        """
        with self.assertRaises(ValidationError):
            x = TestIntegerListFieldModel(int_list_field=['testing'])
            x.save()

    def test_choice_validation_success(self):
        """Test validating a ListField with choices."""
        x = TestIntegerListFieldModel()
        x.int_list_field_choices = [7, 9]
        x.save()

    def test_choice_validation_error(self):
        """Test validating a IntegerListField with choices that throws a
        ValidationError for not having a valid choice."""
        x = TestIntegerListFieldModel()

        with self.assertRaises(ValidationError):
            x.int_list_field_choices = [1, 2]

    def test_choice_validation_out_of_range(self):
        """Test validating a IntegerListField with choices that throws a
        ValidationError for being out of min and max value range."""
        x = TestIntegerListFieldModel()

        with self.assertRaises(ValidationError):
            x.int_list_field_choices = [-1, 50, 101]
