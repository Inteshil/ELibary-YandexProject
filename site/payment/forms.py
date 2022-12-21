from django import forms

from payment.models import PurchasedBook
from core.forms import FormStyleMixin


class BuyBookForm(forms.ModelForm, FormStyleMixin):
    first_name = forms.CharField(label='Имя', max_length=50)
    second_name = forms.CharField(label='Фамилия', max_length=50)

    class Meta:
        model = PurchasedBook
        fields = tuple()
