
from django import forms

from registration.models import CustomUser
from products.models import Product
from categories.models import Category
from accounts.models import Account
from orders.models import Order

# CustomUser Model Forms
class ManageCustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser

        # Editable
        fields = ['status']
        # Show as details
        # 'username', 'id', 'email', 'is_staff', 'is_mod',

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label
            self.fields[field].help_text = False


# Account Model Forms
class ManageAccountForm(forms.ModelForm):
    class Meta:
        model = Account

        # Editable
        fields = ['image']

        # Show as details
        # [ 'user', 'id', 'phone' ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label
            self.fields[field].help_text = False

    def clean(self):
        data = self.cleaned_data
        if not data['image']:
            # default categories image.
            data['image'] = 'accounts/defaults/default-icon.jpg'


# Product Model Forms
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

class ManageProductForm(forms.ModelForm):
    class Meta:
        model = Product

        # Editable
        fields = [
            'category', 'name', 'title', 'description', 'image', 'quantity', 'has_discount', 'active'
        ]

        # shown as details
        # 'id','author', 'price', 'created_at', 'updated_at', 'slug'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label
            self.fields[field].help_text = False

    def clean(self):
        data = self.cleaned_data
        if not data['image']:
            # default categories image.
            data['image'] = 'products/defaults/default-icon.jpg'


# Category Model Forms
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
                ctx['class'] += '' # <- here

            self.fields[field].widget.attrs.update(ctx)

class ManageCategoryForm(forms.ModelForm):
    class Meta:
        model = Category

        # Editable
        fields = [
            'title', 'description', 'image', 'active'
        ]

        # shown as details
        # 'id', 'name', 'author', 'created_at', 'updated_at', 'slug'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label
            self.fields[field].help_text = False

    def clean(self):
        data = self.cleaned_data
        if not data['image']:
            # default categories image.
            data['image'] = 'categories/defaults/default-icon.jpg'


# Order Model Forms
class ManageOrderForm(forms.ModelForm):
    class Meta:
        model = Order

        # Editable
        fields = ['status', 'shipping_method', 'shipping_cost']

        # Show as details
        # ['client', 'items', 'order_type', 'unit_price', 'total_price',
        #  'created_at','updated_at', 'payment_method', 'transaction_id',
        #  'total_amount', 'tracking_number', 'slug']


    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label
            self.fields[field].help_text = False
