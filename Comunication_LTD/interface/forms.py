from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password, get_default_password_validators
from interface.models import CustomUser,Customer,CustomUserPasswordHistory
from django.contrib.auth.hashers import check_password
from config import sec_lvl,db_name
from django.db import connection
from django.contrib.auth.forms import PasswordChangeForm

import datetime

def is_common_password(password: str):
    if password in forbidden_passwords:
        raise ValidationError(
            ('Your password is too weak!'),
            params={'value': password},
        )

DISPLAY_CHOICES = (
    ("High", "High"),
    ("Low", "Low")
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

class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match.")
    }
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.TextInput(attrs={
            'placeholder': ('Password'),
            'class': 'form-control fadeIn second m-2 shadow-sm control-label',
            'onfocus': "this.placeholder=''",
            'onblur': "this.placeholder='Password'",
            'type': 'password',
        }))
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        widget=forms.TextInput(attrs={
            'placeholder': ('Password'),
            'class': 'form-control fadeIn second m-2 shadow-sm control-label',
            'onfocus': "this.placeholder=''",
            'onblur': "this.placeholder='Password'",
            'type': 'password',
        }))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            else:
                validate_password(password1, self.user)

        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])

        if commit:
            self.user.save()

        return self.user

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
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = CustomUser
        fields = ('email', )

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

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=("Old password"),
        widget=forms.TextInput(attrs={
            'placeholder': ('Enter old password'),
            'class': 'form-control fadeIn second m-2 shadow-sm control-label',
            'onfocus': "this.placeholder=''",
            'onblur': "this.placeholder='Enter old password'",
            'type': 'password',
        }))
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.TextInput(attrs={
            'placeholder': ('Password'),
            'class': 'form-control fadeIn second m-2 shadow-sm control-label',
            'onfocus': "this.placeholder=''",
            'onblur': "this.placeholder='Password'",
            'type': 'password',
        }))
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        widget=forms.TextInput(attrs={
            'placeholder': ('Password'),
            'class': 'form-control fadeIn second m-2 shadow-sm control-label',
            'onfocus': "this.placeholder=''",
            'onblur': "this.placeholder='New password confirmation'",
            'type': 'password',
        }))