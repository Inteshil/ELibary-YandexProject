from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from quote.models import Quote
from catalog.models import Book


class QuoteCatalog(ListView):
    template_name = 'quote/quote_list.html'
    queryset = Quote.objects.for_catalog()
    context_object_name = 'quotes'
    extra_context = {
        'page_title': 'Список цитат'
    }


class UserQuoteCatalog(LoginRequiredMixin, ListView):
    template_name = 'quote/user_quote_list.html'
    context_object_name = 'quotes'
    queryset = Quote.objects.all()
    extra_context = {
        'page_title': 'Ваши цитаты'
    }

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


@login_required
def create_quote(request, *args, **kwargs):
    if request.method != 'POST' or not 'quote' in request.POST:
        return HttpResponseNotFound()
    book = get_object_or_404(Book, pk=kwargs['book_id'])
    text = request.POST['quote']
    Quote.objects.create(
        user=request.user,
        book=book,
        text=text
    )
    return redirect('catalog:book_chapter', book_id=kwargs['book_id'], chapter_id=kwargs['chapter_id'])
