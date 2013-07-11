# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext


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
