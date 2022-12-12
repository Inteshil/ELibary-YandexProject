from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'static_pages/index.html'
    extra_context = {
        'page_title': 'Главная'
    }


class AboutPageView(TemplateView):
    template_name = 'static_pages/about.html'
    extra_context = {
        'page_title': 'О проекте'
    }
