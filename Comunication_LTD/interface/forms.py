from django import forms
from config import password_pattern,min_password_length
from django.core.exceptions import ValidationError


def minmin_password_length(value):
    print(int(min_password_length))
    if len(value) < int(min_password_length):
        raise ValidationError(
            ('The password must be minimum 8 characters'),
            params={'value': value},
        )

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
    password = forms.CharField(validators=[minmin_password_length],label=('password'), widget=forms.TextInput(attrs={
        'placeholder':('Password'),
        'class': 'form-control fadeIn second m-2 shadow-sm',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='password'",
        'type': 'password',
        # 'pattern' : password_pattern

    }))

