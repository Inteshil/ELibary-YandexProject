from django.urls import path

from quote.views import QuoteCatalog, UserQuoteCatalog

app_name = 'quote'

urlpatterns = [
    path('', QuoteCatalog.as_view(), name='list'),
    path('user/', UserQuoteCatalog.as_view(), name='user_list'),
]
