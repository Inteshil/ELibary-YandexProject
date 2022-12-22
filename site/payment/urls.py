from django.urls import path

from payment.views import BuyBookView, SuccessView

app_name = 'payment'

urlpatterns = [
    path('buy_book/<int:book_id>/', BuyBookView.as_view(), name='buy_book'),
    path('success/', SuccessView.as_view(), name='success'),
]
