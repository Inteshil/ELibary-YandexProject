from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages

from reports.forms import ReportForm
from catalog.models import Book


class CreateReport(LoginRequiredMixin, CreateView):
    template_name = 'base_form.html'
    form_class = ReportForm
    extra_context = {
        'page_title': 'Создать жалобу',
        'form_title': 'Пожаловаться',
        'button_text': 'Создать жалобу',
    }

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.book = get_object_or_404(
                Book.objects.exclude(author=self.request.user),
                id=kwargs['book_id']
            )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.sender = self.request.user
        self.object.book = self.book
        self.object.save()
        messages.add_message(
            self.request, messages.INFO,
            'Вы успешно подали жалобу. Вскоре модераторы рассмотрят её',
            extra_tags='alert-info',
        )
        return super().form_valid(form)

    def get_success_url(self):
        return self.book.get_absolute_url()
