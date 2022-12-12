from django.urls import path

from catalog.views import CatalogView, BookDetailView

app_name = 'catalog'

urlpatterns = [
    path('', CatalogView.as_view(), name='list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
]
