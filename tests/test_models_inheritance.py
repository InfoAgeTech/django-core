from __future__ import unicode_literals

from datetime import datetime
from random import randint

from django_core.utils.random_utils import random_alphanum
from django_testing.testcases.users import SingleUserTestCase

from test_objects.models import TestManyToManyRelationModel
from test_objects.models import TestModel


class ModelTests(SingleUserTestCase):

    def test_copy1(self):
        test_model = TestModel.objects.create(
            created_user=self.user,
            some_unique_field=random_alphanum(),
            some_unique_field_blank=random_alphanum(),
            some_unique_field_default=random_alphanum()
        )

        test_model_copy = test_model.copy()

        utcnow = datetime.utcnow()
        self.assertIsNone(test_model_copy.id)
        self.assertTrue(test_model_copy.created_dttm <= utcnow)
        self.assertTrue(test_model_copy.last_modified_dttm <= utcnow)
        self.assertEqual(test_model_copy.last_modified_user,
                         test_model_copy.created_user)
        self.assertIsNone(test_model_copy.some_unique_field)
        self.assertIsNone(test_model_copy.some_unique_field_blank)
        self.assertEqual(test_model_copy.some_unique_field_default,
                         'Hello world')

    def test_copy_override_fields(self):
        """Test overriding fields with the model's .copy method."""
        test_model = TestModel.objects.create(
            created_user=self.user,
            some_unique_field=random_alphanum(),
            some_unique_field_blank=random_alphanum(),
            some_unique_field_default=random_alphanum()
        )

        some_string_w_default = random_alphanum()
        some_int = randint(1, 1000)
        some_string_no_default = random_alphanum()
        some_boolean = False
        some_unique_field = random_alphanum()
        some_unique_field_blank = random_alphanum()
        some_unique_field_default = random_alphanum()

        test_model_copy = test_model.copy(
            some_string_w_default=some_string_w_default,
            some_int=some_int,
            some_string_no_default=some_string_no_default,
            some_boolean=some_boolean,
            some_unique_field=some_unique_field,
            some_unique_field_blank=some_unique_field_blank,
            some_unique_field_default=some_unique_field_default
        )

        self.assertEqual(test_model_copy.some_string_w_default,
                         some_string_w_default)
        self.assertEqual(test_model_copy.some_int, some_int)
        self.assertEqual(test_model_copy.some_string_no_default,
                         some_string_no_default)
        self.assertEqual(test_model_copy.some_boolean, some_boolean)
        self.assertEqual(test_model_copy.some_unique_field, some_unique_field)
        self.assertEqual(test_model_copy.some_unique_field_blank,
                         some_unique_field_blank)
        self.assertEqual(test_model_copy.some_unique_field_default,
                         some_unique_field_default)

    def test_copy_exclude_fields(self):
        """Test the models copy method with excluding fields. When passing an
        excluded fields list, the value will become None or the models default
        for that field.
        """
        test_model = TestModel.objects.create(
            created_user=self.user,
            some_unique_field=random_alphanum(),
            some_unique_field_blank=random_alphanum(),
            some_unique_field_default=random_alphanum()
        )

        exclude_fields = [
            'some_string_w_default',
            'some_int',
            'some_string_no_default',
            'some_boolean',
            'some_unique_field',
            'some_unique_field_blank',
            'some_unique_field_default'
        ]

        test_model_copy = test_model.copy(exclude_fields=exclude_fields)

        self.assertEqual(test_model_copy.some_string_w_default, 'hello')
        self.assertEqual(test_model_copy.some_int, 5)
        self.assertIsNone(test_model_copy.some_string_no_default)
        self.assertTrue(test_model_copy.some_boolean)
        self.assertIsNone(test_model_copy.some_unique_field)
        self.assertIsNone(test_model_copy.some_unique_field_blank)
        self.assertEqual(test_model_copy.some_unique_field_default,
                         'Hello world')

    def test_get_many_to_many_model(self):
        """Test for getting a many to many model field."""
        obj = TestManyToManyRelationModel.objects.create(created_user=self.user)
        self.assertEqual(obj.__class__._get_many_to_many_model('m2m_field'),
                         TestModel)
