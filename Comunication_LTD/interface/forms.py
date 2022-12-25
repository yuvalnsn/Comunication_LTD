from django import forms
from config import password_pattern,min_password_length,forbidden_passwords
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from interface.models import CustomUser,Customer

def is_common_password(password: str):
    if password in forbidden_passwords:
        raise ValidationError(
            ('Your password is too weak!'),
            params={'value': password},
        )


class LoginForm(forms.Form):
    username = forms.CharField(label=('Username'), widget=forms.TextInput(attrs={
        'placeholder':('Username'),
        'class': "form-control fadeIn second m-2 shadow-sm control-label",
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='Username'",
    }))
    password = forms.CharField(label=('Password'), widget=forms.TextInput(attrs={
        'placeholder':('Password'),
        'class': 'form-control fadeIn second m-2 shadow-sm control-label',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='password'",
        'type': 'password',
    }))


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label=('Username'), widget=forms.TextInput(attrs={
        'placeholder': ('Username'),
        'class': "form-control fadeIn second m-2 shadow-sm control-label",
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='Username'",
    }))
    email = forms.CharField(label=('Email'), widget=forms.TextInput(attrs={
        'placeholder': ('Email'),
        'class': 'form-control fadeIn second m-2 shadow-sm control-label',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='Email'",
        'type': 'email',
    }))
    password1 = forms.CharField(label=('Password'), widget=forms.TextInput(attrs={
        'placeholder': ('Password'),
        'class': 'form-control fadeIn second m-2 shadow-sm control-label',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='Password'",
        'type': 'password',

    }))
    password2 = forms.CharField(label=('Password confirmation'), widget=forms.TextInput(attrs={
        'placeholder': ('Password'),
        'class': 'form-control fadeIn second m-2 shadow-sm control-label',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='Password'",
        'type': 'password',
    }))

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = True
        self.fields['password2'].required = True
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(SetPasswordForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class registerCustomerForm(forms.Form):
    firstName = forms.CharField(label=('first name'), widget=forms.TextInput(attrs={
            'placeholder':('first name'),
            'class': "form-control fadeIn second m-2 shadow-sm",
            'onfocus': "this.placeholder=''",
            'onblur': "this.placeholder='firstName'"
        }))
    lastName = forms.CharField(label=('last name'), widget=forms.TextInput(attrs={
            'placeholder':('last name'),
            'class': "form-control fadeIn second m-2 shadow-sm",
            'onfocus': "this.placeholder=''",
            'onblur': "this.placeholder='lastName'"
        }))
