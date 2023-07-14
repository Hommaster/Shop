from django import forms

from localflavor.ru.forms import RUPostalCodeField

from .models import Order


class OrderForm(forms.ModelForm):
    postal_code = RUPostalCodeField

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email',
                  'address', 'city', 'postal_code']
