# -*- coding: utf-8 -*-
from django.db import models
from django_core.models import AbstractBaseModel


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
