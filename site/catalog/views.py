from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.urls import reverse

from catalog.models import Book
from rating.models import BookRating
from catalog.models import BookChapter


class CatalogView(ListView):
    template_name = 'catalog/book_list.html'
    queryset = Book.objects.enabled()
    extra_context = {
        'page_title': 'Каталог'
    }
    context_object_name = 'books'


class BookDetailView(DetailView):
    template_name = 'catalog/book_detail.html'
    queryset = Book.objects.enabled()
    pk_url_kwarg = 'book_id'
    context_object_name = 'book'
    extra_context = {
        'title_name': 'Детали книги'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_rating = BookRating.objects.get_rating_of_book(self.object)
        user_rating = BookRating.objects.get_rating_of_user(
            self.object, self.request.user
            )
        if user_rating:
            rate = int(user_rating.rating)
        else:
            rate = None
        return {
            **context,
            'book_rating_avg': str(book_rating['book_rating_avg'])[:4],
            'book_rating_num': book_rating['book_rating_num'],
            'user_rating': rate
        }

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        def sub():
            if not 'rate' in request.POST:
                return
            try:
                rate = int(request.POST['rate'][0])
            except:
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
        return HttpResponseRedirect(reverse('catalog:book_detail', kwargs={'book_id': kwargs['book_id']}))


class BookChapterView(DetailView):
    template_name = 'catalog/book_chapter.html'
    queryset = BookChapter.objects.published()
    pk_url_kwarg = 'chapter_id'
    context_object_name = 'chapter'

    def get_object(self):
        return super().get_object(
            self.queryset.filter(book_id=self.kwargs['book_id'])
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['neighboring_chapters'] = (
            self.object.get_neighboring_chapters()
            )
        return context
