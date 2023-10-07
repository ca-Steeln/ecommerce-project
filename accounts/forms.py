
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse

from .models import Account


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = False
            self.fields[field].help_text = False
            self.fields[field].widget.attrs['readonly'] = True



class AccountForm(forms.ModelForm):

    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput, error_messages={'required':'Password field is required.'})

    class Meta:
        model = Account
        fields = ['phone', 'password']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                'placeholder': self.fields[field].label or field.title(),
            }
            self.fields[field].label = ''
            self.fields[field].widget.attrs.update(ctx)