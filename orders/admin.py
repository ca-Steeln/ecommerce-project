
from django.contrib import admin

from .models import Order

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = [
        'client', 'status', 'order_type', 'total_price' , 'total_amount', 'payment_method','created_at',
        ]


admin.site.register(Order, OrderAdmin)