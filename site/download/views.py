from catalog.models import Book, BookChapter
from django.shortcuts import get_object_or_404, render


def download_book_txt(request, book_id):
    template_name = 'download/txt.txt'
    book = get_object_or_404(Book, pk=book_id)
    chapters, _ = BookChapter.objects.bought_required(
        request.user, book_id
    )
    context = {
        'book': book,
        'chapters': chapters
    }
    response = render(
        request, template_name, context,
        content_type='text/plain; charset=utf-8'
        )
    response.headers['Content-Disposition'] = \
        f'attachment; filename="{book_id}.txt"'
    return response
