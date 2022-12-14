from django.views.generic import ListView, DetailView

from catalog.models import Book, BookChapter


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
