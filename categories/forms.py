
from django import forms

from .models import Category

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
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
                ctx['class'] = ctx["class"] + '' # here

            self.fields[field].widget.attrs.update(ctx)


class UpdateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'title', 'description', 'image', 'active']

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
                ctx['class'] = ctx["class"] + '' # here

            self.fields[field].widget.attrs.update(ctx)

    def clean(self):
        data = self.cleaned_data
        if not data['image']:
            # default categories image.
            data['image'] = 'categories/default/categories-default-icon.jpg'

        return data