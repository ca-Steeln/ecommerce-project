
from django.contrib import admin
from .models import Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at', 'active']
    search_fields = ['id', 'name', 'title']
admin.site.register(Category, CategoryAdmin)