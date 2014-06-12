from __future__ import unicode_literals

from django import forms
from django.forms.util import ErrorDict
from django.forms.widgets import HiddenInput


class PrefixFormMixin(forms.ModelForm):
    """Form mixin for prefix.  Many forms rendered to a page will require a
    prefix to maintain uniqueness with rendering.  This stores the prefix
    used to assist with this.
    """
    form_prefix = forms.CharField(max_length=50, required=False,
                                  widget=HiddenInput)

    def __init__(self, *args, **kwargs):
        # TODO: Data can be in kwargs or it's the first arg param
        if kwargs.get('prefix') is None and 'data' in kwargs:
            for key, val in kwargs.get('data', {}).items():
                if key.endswith('form_prefix'):
                    kwargs['prefix'] = val
                    break

        super(PrefixFormMixin, self).__init__(*args, **kwargs)


class DeleteFormMixin(forms.ModelForm):
    """Delete form mixin when a delete field is needed.  This also prevents
    a form from saving when the delete field is set to true since it should be
    deleted.
    """

    delete = forms.BooleanField(initial=False, required=False,
                                widget=forms.HiddenInput)

    def is_valid(self):
        if (hasattr(self, 'cleaned_data') and
            self.cleaned_data.get('delete') == True):
            return True

        return super(DeleteFormMixin, self).is_valid()

    def clean(self):
        cleaned_data = super(DeleteFormMixin, self).clean()

        # If this object is set to be deleted, validation doesn't matter
        # because the object will be delete anyway so remove all errors so it
        # passes validation.

        if self.cleaned_data.get('delete') == True:
            self._errors = ErrorDict()

        return cleaned_data

    def save(self, *args, **kwargs):
        if self.cleaned_data.get('delete') == True:
            # saving is not allowed for forms that have delete set to true
            return None

        return super(DeleteFormMixin, self).save(*args, **kwargs)
