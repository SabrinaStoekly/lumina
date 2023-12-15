from django import forms
from .models import Order

def set_form_attributes(form_class, placeholders):
    class CustomForm(form_class):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['full_name'].widget.attrs['autofocus'] = True
            for field in self.fields:
                if self.fields[field].required:
                    placeholder = f'{placeholders.get(field, field.capitalize())} *'
                else:
                    placeholder = placeholders.get(field, field.capitalize())
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = 'stripe-style-input'
                self.fields[field].label = False

    return CustomForm

class OrderForm(set_form_attributes(forms.ModelForm, {
    'full_name': 'Full Name',
    'email': 'Email Address',
    'phone_number': 'Phone Number',    
    'postcode': 'Postal Code',
    'town_or_city': 'Town or City',
    'street_address1': 'Street Address 1',
    'street_address2': 'Street Address 2',
    'county': 'County, State or Locality',
})):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode',
                  'county',)
