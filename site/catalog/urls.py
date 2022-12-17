from django.urls import path

from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('', views.CatalogView.as_view(), name='list'),
    path('author/', views.AuthorCatalogView.as_view(), name='author_list'),
]

book_crud = [
    path(
        'book/<int:book_id>/', views.BookDetailView.as_view(),
        name='book_detail'
        ),

    path('create/', views.CreateBookView.as_view(), name='create_book'),
    path(
        'book/<int:book_id>/update/', views.UpdateBookView.as_view(),
        name='update_book'
        ),
    path(
        'book/<int:book_id>/delete/', views.DeleteBookView.as_view(),
        name='delete_book'
        ),
]

book_chapter_crud = [
    path(
        'book/<int:book_id>/<int:chapter_id>/',
        views.BookChapterView.as_view(),
        name='book_chapter'
        ),
    path(
        'book/<int:book_id>/create/', views.CreateChapterView.as_view(),
        name='create_chapter'
        ),
    path(
        'book/<int:book_id>/<int:chapter_id>/update/',
        views.UpdateChapterView.as_view(),
        name='update_chapter'
        ),
    path(
        'book/<int:book_id>/<int:chapter_id>/delete/',
        views.DeleteChapterView.as_view(),
        name='delete_chapter'
        ),
]


urlpatterns += book_chapter_crud + book_crud
