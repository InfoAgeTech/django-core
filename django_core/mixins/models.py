# -*- coding: utf-8 -*-
from django.db import models
from django.utils.html import escape
from django.utils.safestring import mark_safe


class AbstractUrlLinkModelMixin(models.Model):
    """Mixin for accessing the links for the models.  This requires the object
    to have already implemented the following methods:

    * get_absolute_url - returns the absolute link to the object.
    * get_edit_url - returns the link to edit the object
    * get_delete_url - return the link to delete the object.
    """

    class Meta:
        abstract = True

    def get_absolute_url_link(self, text=None):
        """Gets the html link for the object."""
        return mark_safe(u'<a href="{0}">{1}</a>'.format(
                            self.get_absolute_url(),
                            escape(text if text is not None else self.id)))

    def get_edit_url_link(self, text=None):
        """Gets the html edit link for the object."""
        return mark_safe(u'<a href="{0}">{1}</a>'.format(
                            self.get_edit_url(),
                            escape(text if text is not None else 'Edit')))

    def get_delete_url_link(self, text=None):
        """Gets the html delete link for the object."""
        return mark_safe(u'<a href="{0}">{1}</a>'.format(
                            self.get_delete_url(),
                            escape(text if text is not None else 'Delete')))
