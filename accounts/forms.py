
from django import forms

from registration.models import CustomUser

from .models import Account


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = False
            self.fields[field].help_text = False
            self.fields[field].widget.attrs['readonly'] = True



class AccountForm(forms.ModelForm):

    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput, error_messages={'required': 'Password field is required.'})


    class Meta:
        model = Account
        fields = ['phone', 'image', 'password']

        # these messages doesnt show up
        error_messages = {
            'phone': {
                'unique': 'Phone number is already in use',
            },

            'password': {
                'required': 'Password field is required.',
            },
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                'placeholder': self.fields[field].label or field.title(),
            }
            self.fields[field].label = ''
            self.fields[field].widget.attrs.update(ctx)

    def clean(self):
        data = self.cleaned_data
        if not data['image']:
            # default account image.
            data['image'] = 'accounts/defaults/default-icon.jpg'
        return data