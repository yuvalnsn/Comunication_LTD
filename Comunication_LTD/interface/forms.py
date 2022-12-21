from django import forms
from config import password_pattern,min_password_length,forbidden_passwords
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from interface.models import CustomUser,Customer,CustomUserPasswordHistory
from config import sec_lvl,db_name
from django.db import connection
import datetime

def is_common_password(password: str):
    if password in forbidden_passwords:
        raise ValidationError(
            ('Your password is too weak!'),
            params={'value': password},
        )


class LoginForm(forms.Form):
    username = forms.CharField(label=('Username'), widget=forms.TextInput(attrs={
        'placeholder':('Username'),
        'class': "form-control fadeIn second m-2 shadow-sm",
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='Username'"
    }))
    password = forms.CharField(label=('Password'), widget=forms.TextInput(attrs={
        'placeholder':('Password'),
        'class': 'form-control fadeIn second m-2 shadow-sm',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='password'",
        'type': 'password',
    }))

class SetPasswordForm(forms.Form):
        """
        A form that lets a user change set their password without entering the old
        password
        """
        error_messages = {
            'password_mismatch': ("The two password fields didn't match."),
        }
        new_password1 = forms.CharField(label=("New password"),
                                        widget=forms.PasswordInput)
        new_password2 = forms.CharField(label=("New password confirmation"),
                                        widget=forms.PasswordInput)

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
            return password2

        def save(self, commit=True):
            self.user.set_password(self.cleaned_data['new_password1'])
            if commit:
                if (sec_lvl == 'high'):
                    self.user.save()
                else:
                    print("hii")
                    sqlQuery = f"UPDATE {db_name}.interface_customuser SET password = '{self.cleaned_data['new_password1']}' where username = '{self.user.username}'"
                    if self.user._password_has_been_changed():
                        print(self.user)
                        CustomUserPasswordHistory.remember_password(CustomUser.objects.get(username=self.user))
                    print(sqlQuery)
                    with connection.cursor() as cursor:
                        cursor.execute(sqlQuery)
            return self.user

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = True
        self.fields['password2'].required = True
        self.fields['username'].required = True
        self.fields['email'].required = True
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
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


        ##############

# class registerForm(forms.Form):
#     email = forms.CharField(label=('email'), widget=forms.TextInput(attrs={
#         'placeholder':('Email'),
#         'class': "form-control fadeIn second m-2 shadow-sm",
#         'onfocus': "this.placeholder=''",
#         'onblur': "this.placeholder='Email'"
#     }))
#     username = forms.CharField(label=('username'), widget=forms.TextInput(attrs={
#         'placeholder':('username'),
#         'class': "form-control fadeIn second m-2 shadow-sm",
#         'onfocus': "this.placeholder=''",
#         'onblur': "this.placeholder='username'"
#     }))
#     password = forms.CharField(validators=[is_common_password],min_length=min_password_length,label=('password'), widget=forms.TextInput(attrs={
#         'placeholder':('Password'),
#         'class': 'form-control fadeIn second m-2 shadow-sm',
#         'onfocus': "this.placeholder=''",
#         'onblur': "this.placeholder='password'",
#         'type': 'password',
#         'pattern': password_pattern,
#         'title': 'Use 8 or more characters with a mix of letters, numbers'
#     }))
#
#
#
# class SetPasswordForm2(forms.Form):
#     """
#     A form that lets a user change set their password without entering the old
#     password
#     """
#     error_messages = {
#         'password_mismatch': ('The two password fields didn’t match.'),
#     }
#     new_password1 = forms.CharField(
#         label=("New password"),min_length=min_password_length,
#         validators=[is_common_password],
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#         strip=False,
#         #help_text=password_validators_help_text_html(),
#     )
#     new_password2 = forms.CharField(
#         label=("New password confirmation"),
#         min_length=min_password_length,
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#     )
#
#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super().__init__(*args, **kwargs)
#
#     def clean_new_password2(self):
#         password1 = self.cleaned_data.get('new_password1')
#         password2 = self.cleaned_data.get('new_password2')
#         print(self.user)
#         if password1 and password2:
#             if password1 != password2:
#                 raise ValidationError(
#                     self.error_messages['password_mismatch'],
#                     code='password_mismatch',
#                 )
#         # validate_password(password2, self.user)
#         return password2
#
#     def save(self, commit=True):
#         password = self.cleaned_data["new_password1"]
#         self.user.set_password(password)
#         if commit:
#             self.user.save()
#         return self.user
#
# #
