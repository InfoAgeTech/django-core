from __future__ import unicode_literals

from django.contrib.contenttypes import generic as django_generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from ..managers import GenericManager


class AbstractGenericObject(models.Model):
    """Abstract model class for a generic object."""

    class Meta:
        abstract = True

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = django_generic.GenericForeignKey('content_type',
                                                      'object_id')
    objects = GenericManager()
