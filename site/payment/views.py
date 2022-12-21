from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.urls import reverse_lazy
from django.conf import settings
from django.db.models import Q

from sberbank.service import BankService

from payment.forms import BuyBookForm
from payment.models import PurchasedBook
from catalog.models import Book


class BuyBookView(LoginRequiredMixin, FormView):
    template_name = 'base_form.html'
    form_class = BuyBookForm
    success_url = reverse_lazy('payment:success')
    extra_context = {
        'page_title': 'Купить книгу',
        'form_title': 'Покупка книги',
        'form_description': (
            'Это форма для разработки, на продакшн тут будет платежный шлюз'
            ),
        'button_text': 'Купить',
    }

    def dispatch(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id', None)
        user = self.request.user
        if book_id and user.is_authenticated:
            self.book = get_object_or_404(
                Book.objects.enabled().exclude(
                    Q(author=user) | Q(price=0) |
                    Q(purchased__user__id__contains=user.id)
                    ),
                pk=book_id
                )
        else:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if settings.DEBUG:
            return super().get(request, *args, **kwargs)
        else:
            try:
                amount = self.book.price
                client_id = self.request.user.pk

                svc = BankService('main')

                payment, url = svc.pay(
                    amount, client_id=client_id, description='Оплата книги'
                )
                return redirect(url)
            except Exception:
                pass

    def post(self, request, *args, **kwargs):
        PurchasedBook.objects.create(
            book=self.book, user=self.request.user
        )
        return super().post(request, *args, **kwargs)


class SuccessView(TemplateView):
    template_name = 'payment/success.html'
    extra_context = {
        'page_title': 'Успешная покупка'
    }
