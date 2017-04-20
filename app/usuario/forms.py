from django import forms
from django.contrib.auth.models import User

class RegistroUserForm(forms.Form):

    username = forms.CharField(min_length=5)
    email = forms.EmailField()
    password = forms.CharField(min_length=5, widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())


class EliminarUsuarios:
    username = forms.CharField(min_length=5)
    email = forms.EmailField()

