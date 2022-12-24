from django import forms

from django_summernote.widgets import SummernoteWidget

from core.forms import FormStyleMixin
from reports.models import BookReport


class ReportForm(forms.ModelForm, FormStyleMixin):
    class Meta:
        model = BookReport
        fields = ('reason', 'content')
        widgets = {
            'content': SummernoteWidget()
        }
