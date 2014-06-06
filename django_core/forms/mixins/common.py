from __future__ import unicode_literals

from django import forms
from django.forms.util import ErrorDict


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

    def delete(self):
        self.instance.delete()
