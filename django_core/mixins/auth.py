# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator


class LoginRequiredViewMixin(object):
    """Use this with CBVs to ensure user is logged in."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredViewMixin, self).dispatch(*args, **kwargs)


class StaffRequiredMixin(LoginRequiredViewMixin):
    """Require a logged in Staff member."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied

        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


class SuperuserRequiredMixin(LoginRequiredViewMixin):
    """Require a logged in user to be a superuser."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied

        return super(SuperuserRequiredMixin, self).dispatch(request, *args, **kwargs)
