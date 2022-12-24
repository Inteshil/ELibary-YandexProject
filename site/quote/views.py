from django.views.generic import ListView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages

from quote.models import Quote
from catalog.models import Book


class QuoteCatalog(ListView):
    template_name = 'quote/quote_list.html'
    queryset = Quote.objects.for_catalog()
    context_object_name = 'quotes'
    paginate_by = 5
    extra_context = {
        'page_title': 'Список цитат'
    }


class UserQuoteCatalog(LoginRequiredMixin, ListView):
    template_name = 'quote/user_quote_list.html'
    context_object_name = 'quotes'
    queryset = Quote.objects.all()
    paginate_by = 5
    extra_context = {
        'page_title': 'Ваши цитаты'
    }

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class CreateQuote(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if 'quote' not in request.POST:
            raise Http404()

        text = request.POST['quote']
        if text == '':
            messages.add_message(
                self.request, messages.INFO,
                'Выделите текст, чтобы сохранить цитату',
                extra_tags='alert-info',
            )
        else:
            book = get_object_or_404(Book, pk=kwargs['book_id'])
            Quote.objects.create(
                user=request.user,
                book=book,
                text=text
            )
            messages.add_message(
                self.request, messages.SUCCESS,
                'Вы успешно сохранили цитату',
                extra_tags='alert-success',
            )

        return redirect(
            'catalog:book_chapter',
            book_id=kwargs['book_id'],
            chapter_id=kwargs['chapter_id']
        )


class DeleteQuote(LoginRequiredMixin, DeleteView):
    template_name = 'catalog/confirm.html'
    pk_url_kwarg = 'quote_id'
    success_url = reverse_lazy('quote:user_list')
    extra_context = {
        'page_title': 'Удалить цитату',
        'confirm_title': 'Вы уверены, что хотите удалить цитату?',
        'confirm_message': 'Это действие является необратимым!'
    }

    def get_queryset(self):
        return Quote.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.add_message(
            self.request, messages.INFO,
            'Вы успешно удалили цитату',
            extra_tags='alert-info',
        )
        return response
