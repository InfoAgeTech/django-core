# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.http import Http404
from django_tools.paging import paging

User = get_user_model()


class AbstractBaseModel(models.Model):
    """Base model for other db model to extend.  This class contains common 
    model attributes needed by almost all models.
     
    created = cu = created user.  The user who created this instance.  
    created_dttm = cdt = created datetime.  
    last_modified = lmu = last user to modify this instance 
    last_modified_dttm = udt = updated datetime. Datetime this document was last 
        updated.
    """
    created = models.ForeignKey(User, related_name='+')
    created_dttm = models.DateTimeField(default=datetime.utcnow)
    last_modified = models.ForeignKey(User, related_name='+')
    last_modified_dttm = models.DateTimeField(default=datetime.utcnow)

    class Meta:
        abstract = True
        ordering = ['-created_dttm']

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        """Optional kwargs:
        
        - id_length: the length of characters to use for the id.  Default 
                         is 10.
        """
        self.__class__.save_prep(self)
        super(AbstractBaseModel, self).save(*args, **kwargs)

    @classmethod
    def save_prep(cls, instance_or_instances, **kwargs):
        """Common save functionality for all models.  All documents are 
        assumed to have the following fields:
        
            - id
            - created
            - created_id
            - created_dttm
            - last_modified
            - last_modified_id
            - last_modified_dttm
            
        Optional kwargs:
        
            - id_length: the length of characters to use for the id.  Default 
                         is 10.
        
        """
        if (isinstance(instance_or_instances, models.Model) or
            issubclass(instance_or_instances.__class__, models.Model())):
            instances = [instance_or_instances]
        else:
            instances = instance_or_instances

        utc_now = datetime.utcnow()
        for instance in instances:
            instance.last_modified_dttm = utc_now

            if not instance.id or len(instance.id) < 1:
#                instance.id = available_ids.pop() if available_ids else random_alphanum_id(id_len=id_length)
                instance.created_dttm = utc_now

            if instance.created and not instance.last_modified:
                instance.last_modified = instance.created


    @classmethod
    def get_by_id(cls, id, fields=None, select_related=False):
        """Gets a document by an id.
        
        :param id: id of the document to retrieve.
        :param fields: a tuple of field names to return.  If None, all fields 
            are returned (default).
        """
        criteria = {'id': id}
        return cls._get_one(criteria=criteria,
                            fields=fields,
                            select_related=select_related)

    @classmethod
    def get_by_id_or_404(cls, id, select_related=False):
        """Gets by a instance instance r raises a 404 is one isn't found."""
        obj = cls.get_by_id(id=id, select_related=select_related)

        if obj:
            return obj

        raise Http404

    @classmethod
    def get_by_ids(cls, ids, fields=None, select_related=False):
        """Gets documents by ids.
        
        :param ids: list of ids of documents to return
        :param fields: a tuple of field names to return.  If None, all fields 
            are returned (default).
        """
        if not ids:
            return []

        try:
            query_set = cls.objects.filter(id__in=ids)
            if fields:
                query_set = query_set.only(*fields)

            if select_related:
                return query_set.select_related()

            return list(cls.objects(id__in=ids))
        except cls.DoesNotExist:
            return []

    @classmethod
    def _get_one(cls, criteria, fields=None, select_related=False):
        """
        Gets a single document based on a specific set of criteria.
        
        :param criteria: criteria for the query
        :param fields: a tuple of field names to return.  If None, all fields 
            are returned (default).
        """
        try:
            if fields:
                return cls.objects.get(**criteria).only(*fields)[0]
            return cls.objects.get(**criteria)
        except cls.DoesNotExist:
            return None

    @classmethod
    def _get_many(cls, criteria, page=1, page_size=25, order_by=None,
                  fields=None, select_related=False):
        """
        Gets all documents based on the criteria dictionary passed in.
        
        :param criteria: list of criteria to retrieve documents
        :param order_by: tuple of field names to order by
        :param fields: a tuple of field names to return.  If None, all fields 
            are returned (default).
        :param select_related: boolean indicator that will query for all  
            existing referenced objects on the queryset.
        """
        has_more = False

        try:
            query_set = cls.objects(**criteria)

            if order_by:
                query_set = query_set.order_by(*order_by)

            if fields:
                query_set = query_set.only(*fields)

        except cls.DoesNotExist:
            return [], has_more

        # TODO: need to return a queryset instead of a tuple
        return paging(query_set=query_set,
                      page=page,
                      page_size=page_size,
                      select_related=select_related)

    @classmethod
    def _get_many_to_many_model(cls, field_name):
        """Get the model for the many to many field.
        
        :param field_name: field name to get the model for.
        """

        for field in cls._meta.many_to_many:
            if field.attname == field_name:
                # This is the for_objs model class
                return field.related.parent_model

    def update_field(self, field_name, value, update_user):
        """
        This is an instance method that is used by the __init__ method to create
        instance setters methods for all fields on a class.  So, if a class has
        a field "notes" there will be an instance method called ".set_notes" 
        which calls this method to set the field.
        
        :param field_name: the name of the field to update
        :param value: the value to set the field to
        :param update_user: the user updating the field
        """
        setattr(self, field_name, value)
        self.last_modified_id = update_user.id
        self.last_modified = update_user
        self.save()

    @classmethod
    def insert_many(cls, instances):
        """Inserts many documents into a collection. """
        return cls._insert_many(instances)

    @classmethod
    def _insert_many(cls, instances):
        """
        Insert many documents.  This class is meant to be called inside of a 
        classes "insert_many" method. See BillInstance.insert_many for example.
        
        This is beneficial instead of just calling the standard .insert because
        the .insert doesn't allow ids to be set so it tries to add a MongoID 
        which I don't want.  And since the objects already have IDs, it won't
        allow insertion.  It says call .update instead.
        
        :param instances: list of document to add
        """
        cls.save_prep(instance_or_instances=instances)
        return cls.objects.insert(instances)

    @classmethod
    def delete_by_id(cls, id):
        """Deletes a document by id."""
        return cls.delete_by_ids(ids=[id])

    @classmethod
    def delete_by_ids(cls, ids):
        """Delete objects by ids. 
        
        :param ids: list of objects ids to delete.
        :return: True if objects were deleted.  Otherwise, return False if no 
                objects were found or the delete was not successful.
        """
        try:
            cls.objects.filter(id__in=ids).delete()
            return True
        except cls.DoesNotExist:
            return False
