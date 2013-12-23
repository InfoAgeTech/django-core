from django.db.models.query import QuerySet


class SafeDeleteQuerySet(QuerySet):
    """QuerySet that handles safe delete which is really just updating all
    object to have "is_deleted" field set to True.
    """
    def delete_safe(self, **kwargs):
        # Name sure I'm not trying to set the value of 'is_deleted' twice.
        kwargs.pop('is_deleted', None)
        super(SafeDeleteQuerySet, self).update(is_deleted=True, **kwargs)

    def filter(self, is_deleted=None, *args, **kwargs):
        """Always assume you want the objects that aren't considered deleted.

        :param is_deleted: field boolean indicating if you want to pull back
            the instances that are considered to be deleted.

            * If True, this will only pull back deleted instance
            * if False, this will only pull back instances that aren't deleted
            * if None, pull back all instances regardless of the is_delete
              field value.
        """
        if (is_deleted != None and
            'pk' not in kwargs and
            self.model._meta.pk.name not in kwargs):
            kwargs['is_deleted'] = is_deleted

        return super(SafeDeleteQuerySet, self).filter(*args, **kwargs)

    def get(self, is_deleted=None, *args, **kwargs):
        """When trying to retrieve an object by it's primary key, always
        turn off the is_deleted filter.
        """
        if (is_deleted != None and
            'pk' not in kwargs and
            self.model._meta.pk.name not in kwargs):
            kwargs['is_deleted'] = is_deleted

        return super(SafeDeleteQuerySet, self).get(*args, **kwargs)
