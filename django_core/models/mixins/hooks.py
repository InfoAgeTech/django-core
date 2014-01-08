from django.db import models


class AbstractHookModelMixin(models.Model):
    """Hook for adding additional functionality to a model without having to
    define a new model (proxy or otherwise).  This model mixin merely acts as a
    placeholder for adding things like project specific methods like url
    helpers:

    * get_absolute_url(...)

    If isn't overridden, then everythings functions like normal.
    """
    class Meta:
        abstract = True
