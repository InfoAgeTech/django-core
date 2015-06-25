from datetime import datetime

from django.db import models


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

        return datetime.utcnow() <= self.expires_dttm
