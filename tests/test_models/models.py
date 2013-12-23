# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.db import models
from django_core.models.managers import SafeDeleteManager
from django_core.models.mixins.base import AbstractBaseModel
from django_core.models.mixins.crud import AbstractSafeDeleteModelMixin
from django_core.models.mixins.tokens import AbstractTokenModel

from .managers import BaseTestManager


User = get_user_model()

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
    user = models.ForeignKey(User, null=True, blank=True)
    objects = BaseTestManager()


class TestDeleteModel(AbstractSafeDeleteModelMixin):
    """Test model for safe delete.

    ``group`` field is just used for being able to group tests together when
    creating multiple objects of the same model.
    """
    group = models.CharField(max_length=50, blank=True, null=True)
    objects = SafeDeleteManager()
