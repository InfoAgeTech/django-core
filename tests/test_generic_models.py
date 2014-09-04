from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django_testing.user_utils import create_user

from test_objects.models import GenericObject


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
        """Test get activities for a user."""
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
