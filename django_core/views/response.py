# -*- coding: utf-8 -*-
import json
from copy import deepcopy

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View
from django.forms import Form


class JSONResponseMixin(object):
    """Mixin For returning a json response."""

    def render_to_response(self, context, **kwargs):
        return self.get_json_response(content=context, **kwargs)

    def get_json_response(self, content, **kwargs):
        """Returns a json response object."""

        # Don't care to return a django form or view in the response here.
        # Remove those from the context.
        if isinstance(content, dict):
            response_content = {k:deepcopy(v) for k, v in content.items()
                                if k not in ('form', 'view') or k in ('form', 'view')
                                and not isinstance(v, (Form, View))}
        else:
            response_content = content

        return HttpResponse(content=json.dumps(response_content),
                            content_type='application/json; charset=utf-8',
                            **kwargs)


# TODO: this should go away in favor of JSONResponseMixin above
class JsonResponse(HttpResponse):
    """Returns a HttpResponse that has content that's json encoded. Returns a 
    status of 200.
    
    Response content sample::
    
        {
            notification: "notification html",
            additional_content_key1: additional_content_value1
        }
    
    :param content: a dictionary of content that should be returned with the 
        response.
    :return: HttpResponse with json encoded notification content.
    
    """
    def __init__(self, content, status=200):
        super(JsonResponse, self).__init__(content=json.dumps(content),
                                           mimetype='application/json',
                                           status=status)


def json_response(template):
    """Returns a json response."""
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)

            # httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
            # return HttpResponse(loader.render_to_string(*args, **kwargs), **httpresponse_kwargs)

            return render_to_response(output[1],
                                      output[0],
                                      RequestContext(request),
                                      mimetype='application/json')

        return wrapper
    return renderer
