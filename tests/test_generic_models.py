from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django_core.utils.random_utils import random_alphanum
from tests.test_objects.models import GenericObject


User = get_user_model()


def create_user(username=None, email=None):
    if not username:
        username = random_alphanum()

    if not email:
        email = '{0}@{1}.com'.format(random_alphanum(), random_alphanum())

    return User.objects.create_user(username=username,
                                    email=email)


class GenericObjectModelTests(TestCase):

    def setUp(self):
        super(GenericObjectModelTests, self).setUp()
        self.user = create_user()

    def tearDown(self):
        super(GenericObjectModelTests, self).tearDown()
        self.user.delete()

    def test_create_generic_object(self):
        """Testing adding generic object."""
        generic_object = GenericObject.objects.create(content_object=self.user)

        self.assertEqual(generic_object.object_id, self.user.id)
        self.assertEqual(generic_object.content_type,
                         ContentType.objects.get_for_model(self.user))

    def test_get_or_create_generic(self):
        """Test get notifications for a user."""
        generic_object, is_created = GenericObject.objects.get_or_create_generic(content_object=self.user)

        self.assertTrue(is_created)
        self.assertEqual(generic_object.object_id, self.user.id)
        self.assertEqual(generic_object.content_type,
                         ContentType.objects.get_for_model(self.user))
        self.assertEqual(generic_object.content_object, self.user)

        generic_object, is_created = GenericObject.objects.get_or_create_generic(content_object=self.user)

        self.assertFalse(is_created)
        self.assertEqual(generic_object.object_id, self.user.id)
        self.assertEqual(generic_object.content_type,
                         ContentType.objects.get_for_model(self.user))
        self.assertEqual(generic_object.content_object, self.user)
