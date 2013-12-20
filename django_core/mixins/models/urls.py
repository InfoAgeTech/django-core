# -*- coding: utf-8 -*-
from django.db import models
from django.utils.html import escape

from ...html.builders import build_link


class AbstractUrlLinkModelMixin(models.Model):
    """Mixin for accessing the links for the models.  This requires the object
    to have already implemented the following methods:

    * get_absolute_url - returns the absolute link to the object.
    * get_edit_url - returns the link to edit the object
    * get_delete_url - return the link to delete the object.
    """

    class Meta:
        abstract = True

    def get_absolute_url_link(self, text=None, cls=None, icon_class=None,
                              **attrs):
        """Gets the html link for the object."""
        if text == None:
            text = self.id

        return build_link(href=self.get_absolute_url(),
                          text=text,
                          cls=cls,
                          icon_class=icon_class,
                          **attrs)

    def get_edit_url_link(self, text=None, cls=None, icon_class=None,
                          **attrs):
        """Gets the html edit link for the object."""
        if text == None:
            text = 'Edit'

        return build_link(href=self.get_edit_url(),
                          text=text,
                          cls=cls,
                          icon_class=icon_class,
                          **attrs)

    def get_delete_url_link(self, text=None, cls=None, icon_class=None,
                            **attrs):
        """Gets the html delete link for the object."""
        if text == None:
            text = 'Delete'

        return build_link(href=self.get_delete_url(),
                          text=text,
                          cls=cls,
                          icon_class=icon_class,
                          **attrs)
