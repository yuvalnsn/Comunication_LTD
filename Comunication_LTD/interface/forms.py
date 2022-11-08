from django import forms
from config import password_pattern,min_password_length,forbidden_passwords
from django.core.exceptions import ValidationError

def is_common_password(password: str):
    if password in forbidden_passwords:
        raise ValidationError(
            ('Your password is too weak!'),
            params={'value': password},
        )
# TODO: Implement password history check, and login attempts
# TODO: shoot tuvia in the head

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
    password = forms.CharField(validators=[is_common_password],min_length=min_password_length,label=('password'), widget=forms.TextInput(attrs={
        'placeholder':('Password'),
        'class': 'form-control fadeIn second m-2 shadow-sm',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='password'",
        'type': 'password',
        'pattern': password_pattern,
        'title': 'Use 8 or more characters with a mix of letters, numbers'
    }))

