from django.urls import path

from quote.views import (
    QuoteCatalog, UserQuoteCatalog, CreateQuote, DeleteQuote
    )

app_name = 'quote'

urlpatterns = [
    path('', QuoteCatalog.as_view(), name='list'),
    path('user/', UserQuoteCatalog.as_view(), name='user_list'),
    path(
        'create/<int:book_id>/<int:chapter_id>/', CreateQuote.as_view(),
        name='create'
    ),
    path(
        'delete/<int:quote_id>/', DeleteQuote.as_view(), name='delete'
    ),
]
