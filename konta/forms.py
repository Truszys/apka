from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date, datetime
from django import forms
from .models import Nawyki

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class NawykiForm(ModelForm):
    class Meta:
        model = Nawyki
        widgets = {
            'nazwa': forms.TextInput(attrs={'class': 'form-control'})
        }
        fields = ['nazwa', 'koniec', 'user_id']
