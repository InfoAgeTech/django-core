from django import forms
from django_core.forms.widgets import CommaSeparatedListWidget

from test_objects.models import TestIntegerListFieldModel
from test_objects.models import TestListFieldModel


class TestListFieldForm(forms.ModelForm):

    class Meta:
        model = TestListFieldModel


class TestIntegerListFieldForm(forms.ModelForm):

    class Meta:
        model = TestIntegerListFieldModel


class TestCommaSeparatedListWidgetForm(forms.ModelForm):

    class Meta:
        model = TestIntegerListFieldModel
        fields = ('int_list_field_choices',)
        widgets = {
            'int_list_field_choices': CommaSeparatedListWidget
        }
