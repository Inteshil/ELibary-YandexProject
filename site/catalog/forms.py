from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
<<<<<<< HEAD
from django.urls import reverse_lazy
=======
>>>>>>> 711c3059c99620d7e0d12ed1ba23300ef4ed302f

from django_summernote.widgets import SummernoteWidget

from catalog.models import Book, BookChapter
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
<<<<<<< HEAD
            'tags': FilteredSelectMultiple('теги', False)
=======
            'tags': FilteredSelectMultiple('теги', True)
>>>>>>> 711c3059c99620d7e0d12ed1ba23300ef4ed302f
        }
        labels = {
            'preview': 'Изменить превью',
            'tags': ''
        }

    class Media:
        css = {'all': ['admin/css/widgets.css']}
<<<<<<< HEAD
        js = [reverse_lazy('javascript-catalog')]
=======
        js = ['/admin/jsi18n/']
>>>>>>> 711c3059c99620d7e0d12ed1ba23300ef4ed302f


class ChapterForm(forms.ModelForm, FormStyleMixin):
    class Meta:
        model = BookChapter
        fields = ('name', 'content', 'is_published')
        widgets = {
            'content': SummernoteWidget(),
        }
