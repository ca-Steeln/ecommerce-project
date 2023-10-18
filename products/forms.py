

from django import forms

from .models import Product, ProductItem

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        for field in self.fields:
            ctx = {
                # front-end dev: add class for all input elements
                'class': '', # here
                'placeholder': self.fields[field].label or field.title(),
            }
            if self.fields[field].required:
                # front-end dev: add class for all required input elements
                ctx['class'] += '' # <- here

            self.fields[field].widget.attrs.update(ctx)



class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'title', 'description', 'image', 'price', 'quantity', 'discount', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        for field in self.fields:
            ctx = {
                # front-end dev: add class for all input elements
                'class': '', # here
                'placeholder': self.fields[field].label or field.title(),
            }
            if self.fields[field].required:
                # front-end dev: add class for all required input elements
                ctx['class'] += '' # here

            self.fields[field].widget.attrs.update(ctx)

    def clean(self):
        data = self.cleaned_data
        if not data['image']:
            # default categories image.
            data['image'] = 'products/default/products-default-icon.jpg'

        return data


class ProductItemForm(forms.ModelForm):

    notes = forms.CharField(max_length=256, required=False)

    class Meta:
        model = ProductItem
        fields = ['amount', 'notes']

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
