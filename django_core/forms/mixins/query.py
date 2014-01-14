# -*- coding: utf-8 -*-
from django.forms import Form
from django_core.forms.fields import CharFieldStripped


class QueryFormMixin(Form):
    """Form Mixin for free text query field."""
    q = CharFieldStripped(required=False)
