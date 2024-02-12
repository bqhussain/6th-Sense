from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-text'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text'}))

class PasswordForm(PasswordChangeForm):
    error_messages = {
        'password_mismatch': "Missmatch!",
        'required': "Please enter a password",
        'password_incorrect': "Old password is incorrect",# If you do not require the fieldname in the error message
    }
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text','type':'password'}),label='Old Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text','type':'password'}),label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text','type':'password'}),label='Confirm Password')


        # def clean(self):
    #     new_password1=self.cleaned_data.get('new_password1')
    #     new_password2=self.cleaned_data.get('new_password2')
    #     if new_password2 and new_password1 and new_password2 != new_password1:
    #         raise forms.ValidationError("Passwords don't match")
    #     return self.cleaned_data

# class UserRegisterForm(UserCreationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-text'}))
#     first_name = forms.CharField(required=True, widget=forms.TextInput(
#         attrs={'class': 'input-text', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+',
#                'title': 'Enter Characters Only '}))
#     last_name = forms.CharField(required=True, widget=forms.TextInput(
#         attrs={'class': 'input-text', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+',
#                'title': 'Enter Characters Only '}))
#
#     email = forms.EmailField(widget=forms.TextInput(
#         attrs={
#             'placeholder': 'Enter Email'
#         }
#     ))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text'}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text'}))
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
