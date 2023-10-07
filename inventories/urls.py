
from django.urls import path

from .views import inventory_view, order_inventory, clear_inventory, delete_product

app_name = 'inventories'

urlpatterns = [
    path('', inventory_view, name='inventory'),
    path('clear/', clear_inventory, name='clear'),
    path('products/<slug:product_slug>/delete/', delete_product, name='delete'),
    path('order/', order_inventory, name='order'),

]
