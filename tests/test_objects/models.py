from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django_core.db.models import AbstractTokenModel
from django_core.db.models.fields import IntegerListField
from django_core.db.models.fields import ListField
from django_core.db.models.mixins.base import AbstractBaseModel
from django_core.db.models.mixins.generic import AbstractGenericObject

from test_objects.managers import BaseTestManager


list_field_choices = (('TEST', 'Testing'),
                      ('HELLO', 'Hello'),
                      ('WORLD', 'world'))
int_list_field_choices = ((7, 'Seven'),
                          (8, 'Eight'),
                          (9, 'Nine'))


class TestModel(AbstractBaseModel):
    some_string_w_default = models.CharField(max_length=50, default='hello')
    some_int = models.IntegerField(default=5)
    some_string_no_default = models.CharField(max_length=50)
    some_boolean = models.BooleanField(default=True)
    some_unique_field = models.CharField(max_length=20,
                                         unique=True)
    some_unique_field_blank = models.CharField(max_length=20,
                                               unique=True,
                                               null=True,
                                               blank=True)
    some_unique_field_default = models.CharField(max_length=20,
                                                 unique=True,
                                                 default='Hello world')


class TestManagerModel(AbstractTokenModel, AbstractBaseModel):
    slug = models.SlugField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    objects = BaseTestManager()


class TestListFieldModel(models.Model):
    """Test model for list field."""
    list_field = ListField()
    list_field_not_required = ListField(blank=True, null=True)
    list_field_choices = ListField(choices=list_field_choices, blank=True,
                                   null=True)


class TestIntegerListFieldModel(models.Model):
    """Test model for integer list field."""
    int_list_field = IntegerListField()
    int_list_field_not_required = IntegerListField(blank=True, null=True)
    int_list_field_choices = IntegerListField(choices=int_list_field_choices,
                                              min_value=0,
                                              max_value=100,
                                              blank=True,
                                              null=True)
    int_list_field_min_max = IntegerListField(min_value=0,
                                              max_value=100,
                                              blank=True,
                                              null=True)


class GenericObject(AbstractGenericObject):
    """Test model for a generic object."""


class TestManyToManyRelationModel(AbstractBaseModel):
    """Test model for many to many relations."""
    m2m_field = models.ManyToManyField(TestModel)
