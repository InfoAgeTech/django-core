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

    def get_absolute_url_link(self, text=None, cls=None, icon_class=None,
                              **attrs):
        """Gets the html link for the object."""
        return self.build_link(
                        href=self.get_absolute_url(),
                        text=escape(text if text is not None else self.id),
                        cls=cls,
                        icon_class=icon_class,
                        **attrs)

    def get_edit_url_link(self, text=None, cls=None, icon_class=None,
                          **attrs):
        """Gets the html edit link for the object."""
        return self.build_link(
                        href=self.get_edit_url(),
                        text=escape(text if text is not None else 'Edit'),
                        cls=cls,
                        icon_class=icon_class,
                        **attrs)

    def get_delete_url_link(self, text=None, cls=None, icon_class=None,
                            **attrs):
        """Gets the html delete link for the object."""
        return self.build_link(
                        href=self.get_delete_url(),
                        text=escape(text if text is not None else 'Delete'),
                        cls=cls,
                        icon_class=icon_class,
                        **attrs)

    # TODO: might want to move this into a util file "html helpers"?
    def build_link(self, href, text, cls=None, icon_class=None, **attrs):
        """Builds an html link.

        :param href: link for the anchor element
        :param text: text for the anchor element
        :param attrs: other attribute kwargs

        >> link('xyz.com', 'hello', 'big')
        u'<a href="xyz.com" class="big">hello</a>'
        >> link('xyz.com', 'hello', 'big', 'fa fa-times')
        u'<a href="xyz.com" class="big"><i class="fa fa-times"></i> hello</a>'
        """
        if not attrs:
            attrs = {}

        attrs['href'] = href

        if cls:
            attrs['class'] = cls

        attrs_formatted = u' '.join([u'{0}="{1}"'.format(k, v)
                                     for k, v in attrs.items()])

        icon = u'<i class="{0}"></i> '.format(icon_class) if icon_class else ''

        return mark_safe(u'<a {attrs}>{icon}{text}</a>'.format(
                                                        attrs=attrs_formatted,
                                                        icon=icon,
                                                        text=escape(text)))
