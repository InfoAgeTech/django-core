# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django_tools.managers import CommonManager
from copy import deepcopy
from python_tools.list_utils import make_obj_list

User = get_user_model()


class AbstractBaseModel(models.Model):
    """Base model for other db model to extend.  This class contains common 
    model attributes needed by almost all models.
    
    Fields
    ======
    * created: created user.  The user who created this instance.  
    * created_dttm: created datetime.  
    * last_modified: last user to modify this instance 
    * last_modified_dttm: updated datetime. Datetime this document was last 
        updated.
    """
    created = models.ForeignKey(User, related_name='+')
    created_dttm = models.DateTimeField(default=datetime.utcnow)
    last_modified = models.ForeignKey(User, related_name='+')
    last_modified_dttm = models.DateTimeField(default=datetime.utcnow)
    objects = CommonManager()

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
        return super(AbstractBaseModel, self).save(*args, **kwargs)

    @classmethod
    def save_prep(cls, instance_or_instances):
        """Common save functionality for all models. This can be called with a 
        saved or unsaved instance or one or many objects. This is beneficial 
        when additional process needs to happen before a bulk_create which 
        doesn't explicitly call the .save on each instance being saved. This
        method will go through each object and do necessary presave processing.
        
        This method can be extended by classes and implement this abstact class
        by simply creating the def save_prep method and making sure to call 
        super class method making sure the save_prep method is properly called 
        from each inheriting class:
        
        Example:
        
            @classmethod
            def save_prep(cls, instance_or_instances):
                # Do additional processing for inheriting class
                return super(MyInheritingClass, cls).save_prep(instance_or_instances)
         
        Note: Make sure not to call the save_prep method in the save method of 
        inheriting classes or it will get called twice which likely isn't wanted
        since this Abstract class explicitly calls the save_prep on save().
        
        All objects are assumed to have the following fields:
        
        * id
        * created
        * created_dttm
        * last_modified
        * last_modified_dttm
        
        """
        instances = make_obj_list(instance_or_instances)

        utc_now = datetime.utcnow()
        for instance in instances:
            instance.last_modified_dttm = utc_now

            if not instance.created_dttm:
                instance.created_dttm = utc_now

            if instance.created:
                if (not hasattr(instance, 'last_modified') or
                    not instance.last_modified):
                    instance.last_modified = instance.created

    def copy(self, exclude_fields=None):
        """Returns an unsaved copy of this object with all fields except for:
        
        * id
        * create_dttm
        * last_modified_dttm
        
        """
        if not exclude_fields:
            exclude_fields = []

        exclude_fields += ['id', 'created_dttm', 'last_modified_dttm']
        instance = deepcopy(self)
        instance.last_modified = instance.created

        # unset all the attributes that you don't want copied over
        for field in set(exclude_fields):
            default = self.__class__._meta.get_field_by_name(field)[0].get_default()
            setattr(instance, field, default or None)

        return instance

    @classmethod
    def _get_many_to_many_model(cls, field_name):
        """Get the model for the many to many field.
        
        :param field_name: field name to get the model for.
        """

        for field in cls._meta.many_to_many:
            if field.attname == field_name:
                # This is the for_objs model class
                return field.related.parent_model
