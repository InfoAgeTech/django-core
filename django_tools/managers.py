# -*- coding: utf-8 -*-
from django.db import models
from django.http.response import Http404


class CommonManager(models.Manager):

    def get_by_id(self, id, fields=None):
        """Gets a document by an id.
        
        :param id: id of the document to retrieve.
        :param fields: a tuple of field names to return.  If None, all fields 
            are returned (default).
        """
        criteria = {'id': id}
        return self._get_one(criteria=criteria)

    def get_by_id_or_404(self, id):
        """Gets by a instance instance r raises a 404 is one isn't found."""
        obj = self.get_by_id(id=id)

        if obj:
            return obj

        raise Http404

    def get_by_ids(self, ids):
        """Gets documents by ids.
        
        :param ids: list of ids of documents to return
        :param fields: a tuple of field names to return.  If None, all fields 
            are returned (default).
        """
        return self.filter(id__in=ids)

    def _get_one(self, **criteria):
        """
        Gets a single document based on a specific set of criteria.
        
        :param criteria: criteria for the query
        :param fields: a tuple of field names to return.  If None, all fields 
            are returned (default).
        """
        try:
            return self.get(**criteria)
        except self.model.DoesNotExist:
            return None

    def bulk_create(self, objs, *args, **kwargs):
        """Insert many object at once."""
        self.model.save_prep(instance_or_instances=objs)
        return super(CommonManager, self).bulk_create(*args, **kwargs)

    def delete_by_id(self, id):
        """Deletes a document by id."""
        return self.delete_by_ids(ids=[id])

    def delete_by_ids(self, ids):
        """Delete objects by ids. 
        
        :param ids: list of objects ids to delete.
        :return: True if objects were deleted.  Otherwise, return False if no 
                objects were found or the delete was not successful.
        """
        try:
            self.filter(id__in=ids).delete()
            return True
        except self.model.DoesNotExist:
            return False
