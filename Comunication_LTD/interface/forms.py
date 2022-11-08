from django import forms
from config import password_pattern,min_password_length,forbidden_passwords
from django.core.exceptions import ValidationError


def minmin_password_length(password: str):
    if len(password) < int(min_password_length):
        raise ValidationError(
            ('The password must be minimum 8 characters'),
            params={'value': password},
        )

def is_common_password(password: str):
    if password in forbidden_passwords:
        raise ValidationError(
            ('Your password is too weak!'),
            params={'value': password},
        )
# TODO: Implement password history check, and login attempts
# TODO: fix regex validation (if not working)
class LoginForm(forms.Form):
    email = forms.CharField(label=('email'), widget=forms.TextInput(attrs={
        'placeholder':('Email'),
        'class': "form-control fadeIn second m-2 shadow-sm",
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='Email'"
    }))
    password = forms.CharField(label=('password'), widget=forms.TextInput(attrs={
        'placeholder':('Password'),
        'class': 'form-control fadeIn second m-2 shadow-sm',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='password'",
        'type': 'password',
    }))



class registerForm(forms.Form):
    email = forms.CharField(label=('email'), widget=forms.TextInput(attrs={
        'placeholder':('Email'),
        'class': "form-control fadeIn second m-2 shadow-sm",
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='Email'"
    }))
    username = forms.CharField(label=('username'), widget=forms.TextInput(attrs={
        'placeholder':('username'),
        'class': "form-control fadeIn second m-2 shadow-sm",
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='username'"
    }))
    password = forms.CharField(validators=[minmin_password_length, is_common_password],label=('password'), widget=forms.TextInput(attrs={
        'placeholder':('Password'),
        'class': 'form-control fadeIn second m-2 shadow-sm',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='password'",
        'type': 'password',
        # 'pattern' : password_pattern

    }))

