from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from django_summernote.widgets import SummernoteWidget

from catalog.models import Book, BookChapter, BookComment
from core.forms import FormStyleMixin


class BookForm(forms.ModelForm, FormStyleMixin):
    class Meta:
        model = Book
        fields = (
            'name', 'preview', 'description',
            'age_rating', 'tags', 'is_published',
            )

        widgets = {
            'preview': forms.FileInput(),
            'tags': FilteredSelectMultiple('теги', True)
        }
        labels = {
            'preview': 'Изменить превью',
            'tags': ''
        }

    class Media:
        css = {'all': ['admin/css/widgets.css']}
        js = ['/admin/jsi18n/']


class ChapterForm(forms.ModelForm, FormStyleMixin):
    class Meta:
        model = BookChapter
        fields = ('name', 'content', 'is_published')
        widgets = {
            'content': SummernoteWidget(),
        }


class CommentForm(forms.ModelForm, FormStyleMixin):
    class Meta:
        model = BookComment
        fields = ('text',)
        widgets = {
            'text': SummernoteWidget(),
        }
