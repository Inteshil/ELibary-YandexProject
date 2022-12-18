from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.urls import reverse_lazy

import django_filters as filters
from django_filters.widgets import RangeWidget

from catalog.models import Book, Tag
from core.forms import FormStyleMixin


class IntRangeWidget(RangeWidget):
    template_name = 'catalog/widgets/range_widget.html'

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.widgets = (
            forms.NumberInput(attrs={'placeholder': 'От'}),
            forms.NumberInput(attrs={'placeholder': 'До'}),
        )


class BookFilterForm(FormStyleMixin):
    class Media:
        css = {'all': ['admin/css/widgets.css']}
        js = [reverse_lazy('javascript-catalog')]

    def clean_range(self, slice, min_value, max_value):
        ''' Проверяем и исправляем значения промежутка '''

        raw_range = [slice.start, slice.stop]
        is_range_correct = True

        for idx in range(len(raw_range)):
            if raw_range[idx]:
                if min_value <= raw_range[idx] <= max_value:
                    raw_range[idx] = int(raw_range[idx])
                else:
                    raw_range[idx] = None
                    is_range_correct = False

        start, stop = raw_range

        if start and stop and start > stop:
            start, stop = stop, start

        return start, stop, is_range_correct

    def clean_creation_date(self):
        creation_date_slice = self.cleaned_data['creation_date']

        if creation_date_slice is None:
            return

        start, stop, is_range_correct = self.clean_range(
            creation_date_slice, 1, 9999
            )

        data = self.data.copy()
        data['creation_date_min'], data['creation_date_max'] = start, stop
        self.data = data

        if is_range_correct is False:
            raise ValidationError('Введите корректный год')

        return slice(start, stop)

    def clean_chapter_quantity(self):
        chapter_quantity_slice = self.cleaned_data['chapter_quantity']

        if chapter_quantity_slice is None:
            return

        start, stop, is_range_correct = self.clean_range(
            chapter_quantity_slice, 0, 10000
            )

        data = self.data.copy()
        data['chapter_quantity_min'] = start
        data['chapter_quantity_max'] = stop
        self.data = data

        if is_range_correct is False:
            raise ValidationError('Введите корректное количество глав')

        return slice(start, stop)


class BookFilter(filters.FilterSet):
    name = filters.CharFilter(
        label='Название', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по названию'})
        )
    order = filters.OrderingFilter(
        label='Сортировать по', empty_label='Умолчанию',
        method='filter_order',
        fields=(
            ('name', 'Названию'),
            ('creation_date', 'Дате создания'),
            ('chapter_quantity', 'Количеству глав'),
        )
    )
    age_rating = filters.ChoiceFilter(
        empty_label='Любой', choices=Book.AGE_RATING_CHOICES
        )
    creation_date = filters.RangeFilter(
        label='Год создания', method='filter_creation_date',
        widget=IntRangeWidget()
        )
    chapter_quantity = filters.RangeFilter(
        label='Количество глав', method='filter_chapter_quantity',
        widget=IntRangeWidget()
    )
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects, widget=FilteredSelectMultiple('теги', True),
        label=''
    )

    class Meta:
        model = Book
        form = BookFilterForm
        fields = (
            'name', 'order', 'age_rating', 'creation_date', 'chapter_quantity',
            'tags'
            )

    def filter_creation_date(self, queryset, name, value):
        start, stop = value.start, value.stop
        if start:
            queryset = queryset.filter(creation_date__year__gte=start)
        if stop:
            queryset = queryset.filter(creation_date__year__lte=stop)
        return queryset

    def filter_chapter_quantity(self, queryset, name, value):
        start, stop = value.start, value.stop
        queryset = queryset.annotate(
            chapter_quantity=models.Count('chapters')
            )
        if start:
            queryset = queryset.filter(chapter_quantity__gte=start)
        if stop:
            queryset = queryset.filter(chapter_quantity__lte=stop)
        return queryset

    def filter_order(self, queryset, name, value):
        order_field = 'chapter_quantity'
        if value[0].startswith('-'):
            order_field = '-' + order_field
        return (
            queryset
            .annotate(chapter_quantity=models.Count('chapters'))
            .order_by(order_field)
            )
