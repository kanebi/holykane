from django import forms
from .models import Address
from django_countries.widgets import CountrySelectWidget


class BillingAddressesForm (forms.ModelForm):
    field_order = ['email', 'full_name',
                   'country', 'state', 'city', 'apartment_address', 'zip', 'default', ]
    address_type = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'adr_type', 'hidden': 'true', 'value': 'B'}))

    class Meta:
        exclude = ['user', 'sessionID']
        model = Address


class ShippingAddressesForm (forms.ModelForm):
    field_order = ['email', 'full_name',
                   'country', 'state', 'city', 'apartment_address', 'zip', 'default', ]
    address_type = forms.CharField(

        widget=forms.HiddenInput(attrs={'id': 'adr_type', 'hidden': 'true', 'value': 'S'}))

    class Meta:
        exclude = ['user', 'sessionID']
        model = Address
