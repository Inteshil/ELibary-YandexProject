from django.urls import path

from static_pages.views import HomePageView, AboutPageView

app_name = 'static_pages'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
]
