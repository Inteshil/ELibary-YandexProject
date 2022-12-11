from django.views.generic import ListView, DetailView

from catalog.models import Book


class CatalogView(ListView):
    template_name = 'catalog/book_list.html'
    queryset = Book.objects.enabled()
    extra_context = {
        'page_title': 'Каталог'
    }
    context_object_name = 'books'


class BookDetailView(DetailView):
    template_name = 'catalog/book_detail.html'
    model = Book
