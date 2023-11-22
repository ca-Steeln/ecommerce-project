
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    # phone = forms.IntegerField( required=False , error_messages={'unique': 'Phone number is already in use.',} )

    error_messages = {
        'unique_username': 'Username is already in use.',
        'password_mismatch': 'The passwords didn’t match.',
        'unique_email': 'Email is already in use.',
    }

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        data = self.cleaned_data
        email = data.get('email')

        if email:
            qs = CustomUser.objects.filter(email__icontains=email)
            if qs.exists():
                self.add_error('email', 'Email is already in use.')

        return data

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {

                'placeholder': self.fields[field].label or field.title()
            }
            self.fields[field].label = ''
            self.fields[field].help_text = None
            self.fields[field].widget.attrs.update(ctx)


class LoginForm(AuthenticationForm):

    error_messages = {
    "invalid_login": "Invalid Username or Password."
    }
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                'placeholder': self.fields[field].label or field.title(),
            }
            self.fields[field].label = ''
            self.fields[field].widget.attrs.update(ctx)