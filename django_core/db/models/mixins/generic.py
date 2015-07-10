from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from ..managers import GenericManager


class AbstractGenericObject(models.Model):
    """Abstract model class for a generic object."""

    class Meta:
        abstract = True

    content_type = models.ForeignKey('contenttypes.ContentType')
    object_id = models.PositiveIntegerField(db_index=True, unique=False)
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = GenericManager()
