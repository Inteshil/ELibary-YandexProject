from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from quote.models import Quote


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
