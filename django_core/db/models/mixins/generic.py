from __future__ import unicode_literals

from django.contrib.contenttypes import generic as django_generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from ..managers import GenericManager


class AbstractGenericObject(models.Model):
    """Abstract model class for a generic object.

    IMPORTANT: the db_index has been turned off for the ``content_type`` field.
    Django, by default, creates a single column index for all foreign key
    fields.  In most cases that's fine.  In this case, you'll likely want to
    add a multi column index to the model that consumes this abstract model on
    the following two fields:

    * content_type
    * object_id

    Example:

    class MyModel(AbstractGenericObject):
        class Meta:
            index_together = (('content_type', 'object_id',),)

    This give you the content_type index you're expecting, but also gives you
    the ability to index for a specific object of a particular content type.
    Which will helps your query performance when searching for more specific
    objects.

    This prevents you from having to add unnecessary extra indexes which take
    up more space.

    If you still want the content_type only index, you can still add it to your
    model by doing the following:

    class MyModel(AbstractGenericObject):
        class Meta:
            index_together = (('content_type',),)

    """

    class Meta:
        abstract = True

    # see doc above as to why index it turned off for content type
    content_type = models.ForeignKey(ContentType, db_index=False)
    object_id = models.PositiveIntegerField(db_index=True, unique=False)
    content_object = django_generic.GenericForeignKey('content_type',
                                                      'object_id')
    objects = GenericManager()
