
from django.contrib import admin

from .models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):

    model = Product

    list_editable = [
        'category', 'name', 'title', 'description', 'adminPrice', 'clientPrice', 'vistorPrice', 'quantity', 'discount', 'active', 'image',
    ]
    list_display = [
        'id', 'author', 'category', 'name', 'title', 'description', 'adminPrice', 'clientPrice', 'vistorPrice', 'quantity', 'discount', 'updated_at', 'active', 'created_at', 'slug', 'image',
    ]
    search_fields = ['id', 'name', 'title']

admin.site.register(Product, ProductAdmin)