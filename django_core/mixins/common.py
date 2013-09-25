# -*- coding: utf-8 -*-


class CommonSingleObjectMixin(object):

    def get_object(self, **kwargs):
        """Sometimes preprocessing of a view need to happen before the object
        attribute has been set for a view.  In this case, just return the
        object if it has already been set when it's called down the road since
        there's no need to make another query.
        """
        if hasattr(self, 'object') and self.object:
            return self.object

        obj = super(CommonSingleObjectMixin, self).get_object(**kwargs)
        self.object = obj
        return obj

    def get_queryset(self, select_related=False, **kwargs):
        """Get the related objects queryset.

        :param select_related: boolean if the related objects are wanting to
            be selected. (i.e. query will be made of all related objects.
        """
        queryset = super(CommonSingleObjectMixin, self).get_queryset(**kwargs)

        if select_related:
            return queryset.select_related()

        return queryset
