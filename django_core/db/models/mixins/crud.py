from django.db import models


class AbstractSafeDeleteModelMixin(models.Model):
    """Give a model safe delete logic so an indicator can be set to is_deleted
    and not removed from the database.
    """
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete_safe(self):
        self.is_deleted = True
        self.save()
