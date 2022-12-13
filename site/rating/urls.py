from django.urls import path

from rating.views import CreateBookRating

app_name = 'rating'

urlpatterns = [
    path('<book_id>/', CreateBookRating.as_view(), name='set_rating'),
]
