from django.urls import path

from quote.views import QuoteCatalog, UserQuoteCatalog
from quote.views import create_quote

app_name = 'quote'

urlpatterns = [
    path('', QuoteCatalog.as_view(), name='list'),
    path('user/', UserQuoteCatalog.as_view(), name='user_list'),
    path('create/<int:book_id>/<int:chapter_id>', create_quote, name='create')
]
