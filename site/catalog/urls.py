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
    path(
        'book/<int:book_id>/?comment=<int:comment_page>',
        views.BookDetailView.as_view(),
        name='book_detail_comments'
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
        'book/<int:book_id>/chapter/<int:chapter_id>/',
        views.BookChapterView.as_view(),
        name='book_chapter'
        ),
    path(
        'book/<int:book_id>/chapter/create/',
        views.CreateChapterView.as_view(),
        name='create_chapter'
        ),
    path(
        'book/<int:book_id>/chapter/<int:chapter_id>/update/',
        views.UpdateChapterView.as_view(),
        name='update_chapter'
        ),
    path(
        'book/<int:book_id>/chapter/<int:chapter_id>/delete/',
        views.DeleteChapterView.as_view(),
        name='delete_chapter'
        ),
]

book_comment_crud = [
    path(
        'book/<int:book_id>/comment/create/',
        views.CreateCommentView.as_view(),
        name='create_comment'
        ),
    path(
        'book/<int:book_id>/comment/<int:comment_id>/update/',
        views.UpdateCommentView.as_view(),
        name='update_comment'
        ),
    path(
        'book/<int:book_id>/comment/<int:comment_id>/delete/',
        views.DeleteCommentView.as_view(),
        name='delete_comment'
        ),
]

urlpatterns += book_chapter_crud + book_crud + book_comment_crud
