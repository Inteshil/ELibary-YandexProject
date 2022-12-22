from django.urls import path

from download import views

app_name = 'download'

urlpatterns = [
        path(
            'book/<int:book_id>/txt', views.download_book_txt,
            name='download_book_txt'
        ),
]
