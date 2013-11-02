# -*- coding: utf-8 -*-
from .common import CommonSingleObjectViewMixin
from django.core.exceptions import PermissionDenied
from django.http.response import Http404


class CreatorRequiredViewMixin(CommonSingleObjectViewMixin):
    """Mixin that requires the self.object be created by the authenticated
    user.
    """
    def dispatch(self, request, *args, **kwargs):
        # does self.object exist at this point?
        obj = self.get_object()

        if not obj:
            raise Http404

        if obj.created_user_id != request.user.id:
            raise PermissionDenied

        return super(CreatorRequiredViewMixin, self).dispatch(request,
                                                              *args,
                                                              **kwargs)
