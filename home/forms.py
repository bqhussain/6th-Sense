from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from datetimepicker.widgets import DateTimePicker
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.admin import widgets
from django.conf import settings

from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-text'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'input-text', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+',
               'title': 'Enter Characters Only '}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'input-text', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+',
               'title': 'Enter Characters Only '}))

    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Email'
        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


# class UserRegisterForm(UserCreationForm):
#     first_name = forms.CharField(required=True, widget=forms.TextInput(
#         attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+',
#                'title': 'Enter Characters Only '}))
#     last_name = forms.CharField(required=True, widget=forms.TextInput(
#         attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+',
#                'title': 'Enter Characters Only '}))
#
#     # first_name = forms.CharField(max_length=25)
#     # last_name = forms.CharField(max_length=25)
#
#     email = forms.EmailField(widget=forms.TextInput(
#         attrs={
#             'placeholder': 'Enter Email'
#         }
#     ))
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
#
#     # def save(self):
#     #     user = super().save(commit=False)
#     #     user.is_patient = True
#     #     user.save()
#     #     profile = Profile.objects.create(user=user)
#     #     return user


class DateInput(forms.DateInput):
    input_type = 'date'


class UserUpdateForm(forms.ModelForm):
    # first_name = forms.CharField(max_length=25)
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+',
               'title': 'Enter Characters Only '}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+',
               'title': 'Enter Characters Only '}))
    # last_name = forms.CharField(max_length=25)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    GENDER = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    country = CountryField().formfield()
    gender = forms.ChoiceField(choices=GENDER, initial='m', widget=forms.Select(), required=True)

    class Meta:
        model = Profile
        fields = ['image', 'gender', 'date_of_birth', 'country', 'address', 'city']

        widgets = {'country': CountrySelectWidget(), 'date_of_birth': DateInput()}


class AppointmentRequestForm(forms.Form):
    # AppointmentTime = forms.DateTimeField(widget=forms.TextInput(
    #     attrs={'class':'form-control datetimepicker-input','data-target':'#datetimepicker1','id' : 'datetimepicker1', 'style':'max-width:50%;'}))


    AppointmentTime = forms.DateTimeField(input_formats = ['%d-%m-%Y %H:%M'],
    widget = forms.DateTimeInput(attrs={
        'class': 'form-control datetimepicker-input',
        'data-target': '#datetimepicker1',
        'style': 'max-width:50%;',
    }))

