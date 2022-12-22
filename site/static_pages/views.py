from django.views.generic import TemplateView, ListView

from catalog.models import Book


class HomePageView(ListView):
    template_name = 'static_pages/index.html'
    queryset = Book.objects.enabled().order_by('-rating_count', '-avg_rating')
    context_object_name = 'books'
    extra_context = {
         'page_title': 'Главная'
     }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['should_open_filter'] = len(self.request.GET) != 0
        return context


class AboutPageView(TemplateView):
    template_name = 'static_pages/about.html'
    extra_context = {
        'page_title': 'О проекте'
    }
