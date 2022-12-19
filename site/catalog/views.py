from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView
    )

from django_filters.views import FilterView

from catalog.models import Book, BookChapter, BookComment
from catalog.forms import BookForm, ChapterForm
from catalog.utils import AuthorRequiredMixin
from catalog.filters import BookFilter

from rating.models import BookRating


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
    context_object_name = 'book'
    extra_context = {
        'title_name': 'Детали книги',
        'page_title': 'Книга',
    }

    def get_queryset(self):
        return Book.objects.enabled_for_author(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = BookChapter.objects.for_user(
            self.request.user, self.kwargs['book_id']
            )

        book_rating = BookRating.objects.get_rating_of_book(self.object)
        user_rating = BookRating.objects.get_rating_of_user(
            self.object, self.request.user
            )

        context['user_rating'] = None
        if user_rating:
            context['user_rating'] = int(user_rating.rating)

        context['active_elem'] = 'main'
        comments_paginator = Paginator(
            BookComment.objects.get_comments_for_book(
                self.kwargs['book_id']
                ), 2
            )
        comments_number = self.request.GET.get('comment')
        try:
            context['comments'] = comments_paginator.page(comments_number)
            context['active_elem'] = 'ratings'
        except PageNotAnInteger:
            context['comments'] = comments_paginator.page(1)

        return {**context, **book_rating}

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        book = get_object_or_404(Book, pk=self.kwargs['book_id'])

        def sub():
            if request.user == book.author:
                return
            if 'rate' not in request.POST:
                return
            try:
                rate = int(request.POST['rate'][0])
            except Exception:
                return
            rating = BookRating.objects.get_rating_of_user(
                self.kwargs['book_id'], self.request.user
            )
            self.object = self.get_object()
            if rating is None:
                self.object = BookRating()
                self.object.book_id = self.kwargs['book_id']
                self.object.user_id = self.request.user.id
                self.object.rating = rate
                self.object.save()
            else:
                rating.rating = rate
                rating.save()
        sub()
        return redirect('catalog:book_detail', book_id=kwargs['book_id'])


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
