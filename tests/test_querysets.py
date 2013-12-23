# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django_testing.testcases.users import SingleUserTestCase
from python_tools.random_utils import random_alphanum

from .test_models.models import TestDeleteModel


User = get_user_model()


class QuerySetTests(SingleUserTestCase):

    def test_safe_delete(self):
        """Test for making sure the objects in the database aren't deleted."""
        group = random_alphanum()
        obj_1 = TestDeleteModel.objects.create(group=group)
        obj_2 = TestDeleteModel.objects.create(group=group)

        TestDeleteModel.objects.filter(group=group).delete_safe()

        objs = list(TestDeleteModel.objects.filter(group=group,
                                                   is_deleted=None))
        self.assertEqual(len(objs), 2)
        self.assertTrue(obj_1 in objs)
        self.assertTrue(obj_2 in objs)

        self.assertTrue(objs[0].is_deleted)
        self.assertTrue(objs[1].is_deleted)

    def test_delete(self):
        """Test for making sure the objects in the database is deleted."""
        group = random_alphanum()
        TestDeleteModel.objects.create(group=group)
        TestDeleteModel.objects.create(group=group)
        TestDeleteModel.objects.filter(group=group).delete()

        objs = list(TestDeleteModel.objects.filter(group=group))
        self.assertEqual(len(objs), 0)
