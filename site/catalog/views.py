from django.views.generic import ListView, DetailView

from catalog.models import Book
from rating.models import BookRating


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
    pk_url_kwarg = 'pk'
    context_object_name = 'book'
    extra_context = {
        'title_name': 'Детали товара'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = BookRating.objects.get_rating_of_book(self.object)
        if self.request.user.is_authenticated:
            extra_context['user_rating'] = BookRating.objects.filter(
                user=self.request.user, book_id=self.kwargs['pk']
                ).first()
        return {**context, **extra_context}

#class BookDetailView(DetailView):
#    template_name = 'catalog/book_detail.html'
#    model = Book
