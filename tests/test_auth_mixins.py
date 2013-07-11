# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.handlers.wsgi import WSGIHandler
from django.test import Client
from django.test import TestCase
from django_core.mixins.auth import StaffRequiredMixin
from django_core.mixins.auth import SuperuserRequiredMixin
import uuid
from mock import patch

User = get_user_model()

class AuthMixinTests(TestCase):

    def setUp(self):
        super(AuthMixinTests, self).setUpClass()
        self.username = uuid.uuid4().hex
        self.password = uuid.uuid4().hex
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        self.client = Client()

    def tearDown(self):
        super(AuthMixinTests, self).tearDownClass()
        self.user.delete()

    def test_staff_required_mixin_not_staff(self):
        """Test for mixin requiring a staff user when user isn't staff."""
        self.client.login(username=self.username, password=self.password)

        with self.assertRaises(PermissionDenied):
            request = WSGIHandler()
            request.user = self.user

            mixin = StaffRequiredMixin()
            mixin.dispatch(request)

    @patch('django_core.mixins.auth.LoginRequiredMixin.dispatch')
    def test_staff_required_mixin_is_staff(self, dispatch):
        """Test for mixin requiring a staff user when user is staff."""
        dispatch.return_value = 'worked'
        self.client.login(username=self.username, password=self.password)
        self.user.is_staff = True

        request = WSGIHandler()
        request.user = self.user

        mixin = StaffRequiredMixin()
        actual_return = mixin.dispatch(request)

        self.assertEqual(actual_return, dispatch.return_value)

    def test_superuser_required_mixin_not_supersuer(self):
        """Test for mixin requiring a superuser when user isn't a superuser."""
        self.client.login(username=self.username, password=self.password)

        with self.assertRaises(PermissionDenied):
            request = WSGIHandler()
            request.user = self.user

            mixin = SuperuserRequiredMixin()
            mixin.dispatch(request)

    @patch('django_core.mixins.auth.LoginRequiredMixin.dispatch')
    def test_superuser_required_mixin_is_supersuer(self, dispatch):
        """Test for mixin requiring a superuser when user is a superuser."""
        dispatch.return_value = 'worked'

        self.client.login(username=self.username, password=self.password)
        self.user.is_superuser = True

        request = WSGIHandler()
        request.user = self.user

        mixin = SuperuserRequiredMixin()
        actual_return = mixin.dispatch(request)

        self.assertEqual(actual_return, dispatch.return_value)
