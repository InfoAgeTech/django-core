# -*- coding: utf-8 -*-
from django.db import models
from django.http.response import Http404
from django.template.defaultfilters import slugify
from python_tools.random_utils import random_alphanum_id


class BaseManager(models.Manager):

    def get_or_none(self, **kwargs):
        """Gets a single object based on kwargs or None if one is not found."""
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class CommonManager(BaseManager):

    def get_by_id(self, id, fields=None):
        """Gets a document by an id.
        
        :param id: id of the document to retrieve.
        :param fields: a tuple of field names to return.  If None, all fields 
            are returned (default).
        """
        return self.get_or_none(id=id)

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

    def bulk_create(self, objs, *args, **kwargs):
        """Insert many object at once."""
        # TODO: This might be making a bad assumption that this is inheriting
        # from AbstractBaseModel
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


class SlugManager(BaseManager):
    """Manager mixin for slugs."""

    def get_by_slug(self, slug, **kwargs):
        try:
            return self.get(slug=slug, **kwargs)
        except self.model.DoesNotExist:
            return None

    def get_by_slug_or_404(self, slug, **kwargs):
        group = self.get_by_slug(slug, **kwargs)

        if group:
            return group

        raise Http404

    def is_slug_available(self, slug, **kwargs):
        """Checks to see if a slug is available. If the slug is already being used
        this method returns False.  Otherwise, return True.
        """
        try:
            self.get(slug=slug, **kwargs)
            return False
        except self.model.DoesNotExist:
            return True

    def get_next_slug(self, slug, **kwargs):
        """Gets the next available slug.
        
        :param slug: the slug to slugify
        :param kwargs: additional filter criteria to check for when looking for
            a unique slug.
        
        Example:
        
        if the value "my-slug" is already taken, this method will append "-n"
        to the end of the slug until the next available slug is found.
        
        """
        original_slug = slug = slugify(slug)
        count = 0

        while not self.is_slug_available(slug=slug, **kwargs):
            count += 1
            slug = '{0}-{1}'.format(original_slug, count)

        return slug


class TokenManager(BaseManager):
    """Manager Mixin for tokens."""

    def get_by_token(self, token, **kwargs):
        """Get by token."""
        return self.get_or_none(token=token, **kwargs)

    def get_by_token_or_404(self, token, **kwargs):
        group = self.get_by_token(token, **kwargs)

        if group:
            return group

        raise Http404

    def get_next_token(self, length=25, **kwargs):
        """Gets the next available token.
        
        :param kwargs: additional filter criteria to check for when looking for
            a unique token.
        
        """
        while True:
            tokens = [random_alphanum_id(id_len=length) for t in range(5)]
            obj_ids = self.filter(token__in=tokens).values_list('id')
            available = set(tokens).difference(obj_ids)

            if available:
                return available.pop()


class UserManager(models.Manager):
    """Manager Mixin for models that have a user."""

    def get_by_user(self, user, **kwargs):
        return self.get_by_user_id(user_id=user.id, **kwargs)

    def get_by_user_id(self, user_id, **kwargs):
        try:
            return self.filter(user_id=user_id)
        except self.model.DoesNotExist:
            return []
