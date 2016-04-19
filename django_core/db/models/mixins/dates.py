from datetime import datetime

from django.db import models


class AbstractDateTimeTrackingModelMixin(models.Model):
    """Model for tracking created and last modified datetimes."""
    created_dttm = models.DateTimeField(default=datetime.utcnow)
    last_modified_dttm = models.DateTimeField(default=datetime.utcnow)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.id or not self.last_modified_dttm:
            # only update the last_modified_dttm if the object is new or the
            # last modified dttm doesn't exists.
            self.last_modified_dttm = datetime.utcnow()

        return super(AbstractDateTimeTrackingModelMixin, self).save(*args,
                                                                    **kwargs)


class AbstractExpiresModelMixin(models.Model):
    """Model mixin for models that can expire.

    Fields:

    - expires_dttm: the UTC date time that the model object expires.
    """
    expires_dttm = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def is_expired(self):
        """Boolean indicating if the model object has expired or not."""
        if not self.expires_dttm:
            # an object with no expires_dttm won't ever expire
            return False

        return datetime.utcnow() >= self.expires_dttm
