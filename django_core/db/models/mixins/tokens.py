from django.db import models
from django_core.db.models.managers import TokenManager
from python_tools.list_utils import make_obj_list


class AbstractTokenModel(models.Model):

    token = models.CharField(max_length=50, db_index=True, unique=True)
    token_length = 15
    objects = TokenManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Make sure token is added."""
        self.save_prep(instance_or_instances=self)
        return super(AbstractTokenModel, self).save(*args, **kwargs)

    @classmethod
    def save_prep(cls, instance_or_instances, token_length=token_length):
        """Preprocess the object before the object is saved.  This
        automatically gets called when the save method gets called.
        """
        instances = make_obj_list(instance_or_instances)

        tokens = set(cls.objects.get_available_tokens(count=len(instances),
                                                    token_length=token_length))

        for instance in instances:
            if not instance.token:
                instance.token = tokens.pop()

        super(AbstractTokenModel, cls).save_prep(
                                            instance_or_instances=instances)
