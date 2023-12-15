from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # Excluding the 'user' field from the form
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        # Initialize the form with additional attributes
        super().__init__(*args, **kwargs)

        # Define placeholders for form fields
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        # Set autofocus on the first field
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True

        # Loop through form fields
        for field in self.fields:
            # Exclude the 'default_country' field
            if field != 'default_country':
                # Assign placeholder text for each field
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'  # Add '*' for required fields
                else:
                    placeholder = placeholders[field]

                # Apply placeholders and classes to form inputs
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = ('border-black '  # Apply CSS classes
                                                             'rounded-0 '
                                                             'profile-form-input')
                self.fields[field].label = False