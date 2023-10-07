
from django.contrib import admin

from .models import Order

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['id', 'client', 'status', 'created_at', 'updated_at', 'slug']

admin.site.register(Order, OrderAdmin)