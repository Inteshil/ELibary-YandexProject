from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy, reverse
from django.contrib import messages
from django.http import Http404

from django_filters.views import FilterView

from catalog.models import Book, BookChapter
from catalog.forms import BookForm, ChapterForm
from catalog.utils import AuthorRequiredMixin
from catalog.filters import BookFilter


class CatalogView(FilterView):
    template_name = 'catalog/book_list.html'
    queryset = Book.objects.enabled()
    filterset_class = BookFilter
    context_object_name = 'books'
    extra_context = {
        'page_title': 'Каталог'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['should_open_filter'] = len(self.request.GET) != 0
        return context


class AuthorCatalogView(LoginRequiredMixin, CatalogView):
    ''' Список книг автора '''

    template_name = 'catalog/author_book_list.html'

    def get_queryset(self):
        return Book.objects.get_queryset().filter(author=self.request.user)


# Book CRUD

class BookDetailView(DetailView):
    template_name = 'catalog/book_detail.html'
    pk_url_kwarg = 'book_id'
    extra_context = {
        'page_title': 'Книга',
    }

    def get_queryset(self):
        return Book.objects.enabled_for_author(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = BookChapter.objects.for_user(
            self.request.user, self.kwargs['book_id']
            )
        return context


class CreateBookView(LoginRequiredMixin, CreateView):
    template_name = 'base_form.html'
    form_class = BookForm
    extra_context = {
        'page_title': 'Создать книгу',
        'form_title': 'Создать книгу',
        'button_text': 'Создать',
    }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class UpdateBookView(LoginRequiredMixin, UpdateView):
    template_name = 'base_form.html'
    form_class = BookForm
    pk_url_kwarg = 'book_id'
    extra_context = {
        'page_title': 'Настройки книги',
        'form_title': 'Изменить книгу',
        'button_text': 'Сохранить',
    }

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user)


class DeleteBookView(LoginRequiredMixin, DeleteView):
    template_name = 'catalog/confirm.html'
    pk_url_kwarg = 'book_id'
    success_url = reverse_lazy('catalog:author_list')
    extra_context = {
        'page_title': 'Удалить книгу',
        'confirm_title': 'Вы уверены, что хотите удалить книгу?',
        'confirm_message': 'Это действие является необратимым!',
    }

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user)

    def post(self, request, *args, **kwargs):
        messages.add_message(
            self.request, messages.INFO,
            'Вы <strong>успешно</strong> удалили книгу',
            extra_tags='alert-info',
            )
        return super().post(request, *args, **kwargs)


# BookChapter CRUD

class BookChapterView(DetailView):
    template_name = 'catalog/book_chapter.html'
    pk_url_kwarg = 'chapter_id'
    context_object_name = 'chapter'
    extra_context = {
        'page_title': 'Глава'
    }

    def get_object(self):
        queryset = BookChapter.objects.for_user(
            self.request.user, self.kwargs.get('book_id')
            )
        current, self.neighboring_chapters = (
            BookChapter.objects.get_neighboring_chapters(
                queryset, self.kwargs.get('chapter_id')
                )
            )
        if current is None:
            raise Http404('Глава не найдена')
        return current

    def get_queryset(self):
        return BookChapter.objects.for_user(
            self.request.user, self.kwargs['book_id']
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['neighboring_chapters'] = self.neighboring_chapters
        return context


class CreateChapterView(AuthorRequiredMixin, CreateView):
    template_name = 'base_form.html'
    form_class = ChapterForm
    extra_context = {
        'page_title': 'Создать главу',
        'form_title': 'Создать главу',
        'button_text': 'Создать',
    }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.book = self.book
        self.object.number = BookChapter.objects.get_max_number(self.book)
        return super().form_valid(form)


class UpdateChapterView(AuthorRequiredMixin, UpdateView):
    template_name = 'base_form.html'
    form_class = ChapterForm
    pk_url_kwarg = 'chapter_id'
    extra_context = {
        'page_title': 'Настройки главы',
        'form_title': 'Изменить главу',
        'button_text': 'Сохранить',
    }

    def get_object(self):
        return super().get_object(
            BookChapter.objects.filter(book_id=self.kwargs['book_id'])
            )


class DeleteChapterView(AuthorRequiredMixin, DeleteView):
    template_name = 'catalog/confirm.html'
    pk_url_kwarg = 'chapter_id'
    extra_context = {
        'page_title': 'Удалить главу',
        'confirm_title': 'Вы уверены, что хотите удалить главу?',
        'confirm_message': 'Это действие является необратимым!',
    }

    def get_object(self):
        return super().get_object(
            BookChapter.objects.filter(book_id=self.kwargs['book_id'])
            )

    def get_success_url(self):
        self.success_url = reverse(
            'catalog:book_detail', kwargs={'book_id': self.kwargs['book_id']}
            )
        return super().get_success_url()

    def post(self, request, *args, **kwargs):
        messages.add_message(
            self.request, messages.INFO,
            'Вы <strong>успешно</strong> удалили главу',
            extra_tags='alert-info',
            )
        return super().post(request, *args, **kwargs)
