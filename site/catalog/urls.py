from django.urls import path

from catalog.views import CatalogView, BookDetailView, BookChapterView

app_name = 'catalog'

urlpatterns = [
    path('', CatalogView.as_view(), name='list'),
    path('book/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path(
        'book/<int:book_id>/<int:chapter_id>/', BookChapterView.as_view(),
        name='book_chapter'
        ),
]
