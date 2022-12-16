from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from catalog.models import Book


class AuthorRequiredMixin(LoginRequiredMixin):
    ''' Пускаем только автора книги '''

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.book = get_object_or_404(
                Book, id=kwargs['book_id'], author=request.user
                )
        return super().dispatch(request, *args, **kwargs)
