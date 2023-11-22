
from django.contrib import admin

from .models import Product, ProductItem

# Register your models here.

class ProductAdmin(admin.ModelAdmin):

    model = Product

    list_display = [
        'category', 'name', 'price', 'quantity', 'has_discount', 'updated_at', 'active',
    ]
    search_fields = ['id', 'name', 'title']

admin.site.register(Product, ProductAdmin)

class ProductItemsAdmin(admin.ModelAdmin):

    model = ProductItem

    list_display = ['product', 'amount']

admin.site.register(ProductItem, ProductItemsAdmin)