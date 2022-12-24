from django.views.generic import TemplateView, ListView

from catalog.models import Book


class HomePageView(ListView):
    template_name = 'static_pages/index.html'
    queryset = Book.objects.enabled()[:8]
    context_object_name = 'books'
    extra_context = {
         'page_title': 'Главная'
     }


class AboutPageView(TemplateView):
    template_name = 'static_pages/about.html'
    extra_context = {
        'page_title': 'О проекте'
    }
