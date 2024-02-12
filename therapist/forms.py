from django import forms


class TherapistLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class':'input100'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'input100'}
    ))