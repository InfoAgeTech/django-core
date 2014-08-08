from django.db import models


class AbstractHookModelMixin(models.Model):
    """Hook for adding additional functionality to a model without having to
    define a new model (proxy or otherwise).  The primary benefit here is if
    you wanted to add additional fields to a model.  A proxy model won't allow
    for that and non abstract models that are extended require additional
    database lookups to satisfy the one-to-one relationship.

    This is useful in third party applications where you want to extend the
    functionality of a model, but don't own the code.

    If it isn't overridden, then everything functions like normal.

    For an example usage, see:

    https://github.com/InfoAgeTech/django-user-connections/blob/master/django_user_connections/models.py
    """
    class Meta:
        abstract = True
