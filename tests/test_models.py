# -*- coding: utf-8 -*-

from .models import TestModel
from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
import uuid

User = get_user_model()

class ModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ModelTests, cls).setUpClass()
        cls.user = User.objects.create_user(username=uuid.uuid4().hex)

    @classmethod
    def tearDownClass(cls):
        super(ModelTests, cls).tearDownClass()
        cls.user.delete()

    def test_copy(self):
        test_model = TestModel.objects.create(created_user=self.user)
        test_model_copy = test_model.copy()

        utcnow = datetime.utcnow()
        self.assertIsNone(test_model_copy.id)
        self.assertTrue(test_model_copy.created_dttm <= utcnow)
        self.assertTrue(test_model_copy.last_modified_dttm <= utcnow)

        self.assertEqual(test_model_copy.last_modified_user, test_model_copy.created)
