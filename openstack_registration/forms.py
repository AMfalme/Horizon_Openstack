from django import forms
from django.conf import settings

import requests
import json

class UserCreationForm(forms.Form):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'account_creation_failure': "There was a problem creating your account. Please try again!",
    }
    email_address = forms.EmailField(label=('Email Address'), required=True,
        widget=forms.EmailInput(attrs={"autofocus": "autofocus"}))
    password1 = forms.CharField(label=("Password"), required=True, min_length=8,
        widget=forms.PasswordInput,
        help_text=("Must be at least 8 characters"))
    password2 = forms.CharField(label=("Password Confirmation"), required=True,
        min_length=8,
        widget=forms.PasswordInput,
        help_text=("Enter the same password as above, for verification."))

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        email_address =  self.cleaned_data.get('email_address')
        raw_password = self.cleaned_data.get('password1')
        payload = {
            'emailAddress':email_address,
            'password':raw_password
        }
        headers = {'Content-type': 'application/json'}
        response = requests.post(settings.DIAM_USER_URL, data=json.dumps(payload), headers=headers)
        if response.status_code == 201:
            return self.cleaned_data 
        elif response.status_code == 480:
            self.add_error(None, "User already exists. Please login instead")
        else:
            self.add_error(None, "There was a problem creating your account. Please try again")
        
        return self.cleaned_data