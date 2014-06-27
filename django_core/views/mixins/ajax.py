from django.shortcuts import render_to_response
from django.template.context import RequestContext


class AjaxViewMixin(object):
    """View mixin for alternatively returning a different template response
    when the request is made via ajax.
    """

    ajax_template_name = None

    def render_to_response(self, context, **response_kwargs):

        if not self.request.is_ajax():
            return super(AjaxViewMixin,
                         self).render_to_response(context, **response_kwargs)

        return render_to_response(
            self.ajax_template_name,
            context,
            context_instance=RequestContext(self.request)
        )
