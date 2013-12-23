from django.db import models


class AbstractSafeDeleteModelMixin(models.Model):
    """Model mixin for handling deleting an object when you don't necessarily
    want the object to be deleted, but instead just have the "is_deleted"
    field set to True.
    """
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete_safe(self, **kwargs):
        """Delete safe is different from ``delete(...)`` in that it doesn't
        actually delete the object.  It simply sets the ``is_deleted`` indicator
        to True, but doens't remove the object from the database.  If you want
        to remove the object from the database, call the ``delete(...)`` method.
        """
        self.is_deleted = True
        self.save()
