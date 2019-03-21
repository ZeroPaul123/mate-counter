from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')


class RegistrationForm(forms.Form):
    username = forms.CharField(label=('Username'), max_length=30)
    first_name = forms.CharField(label=('First name'), max_length=30)
    last_name = forms.CharField(label=('Last name'), max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label=('Password'),
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label=('Password (Again)'),
                                widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('Passwords do not match.')

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email is already taken.')

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')
