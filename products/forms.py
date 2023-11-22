

from django import forms

from .models import ProductItem


class AddProductItemForm(forms.ModelForm):
    note = forms.CharField(max_length=256, required=False)

    class Meta:
        model = ProductItem
        fields = ['amount', 'note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                # front-end dev: add class for all fields elements
                'class': '', # here
                'placeholder': self.fields[field].label or field.title(),
            }

            if self.fields[field].required:
                # front-end dev: add class for all required input elements
                ctx['class'] += '' # here

            self.fields[field].widget.attrs.update(ctx)


class OrderProductItemForm(AddProductItemForm):
    agreement = forms.BooleanField(required=True)

    class Meta:
        model = ProductItem
        fields = ['amount', 'agreement', 'note']

