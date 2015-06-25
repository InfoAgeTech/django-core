from django.db import models


class AbstractHttpStatusModelMixin(models.Model):
    """Model mixin for objects that can expire.

    Fields:

    - status_code: the http status code
    - status_code_msg: the status code message that accompanies the status code.
    """
    status_code = models.IntegerField(db_index=True, blank=True, null=True)
    status_code_msg = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        abstract = True
