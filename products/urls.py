
from django.urls import path

from .views import (
    products_view, create_product ,product_view , update_product, add_product, order_product, delete_product,
    )

app_name = 'products'

urlpatterns = [
    path('', products_view, name='products'),
    path('create/', create_product, name='create'),
    path('<slug:slug>/', product_view, name='product'),
    path('<slug:slug>/update/', update_product, name='update'),
    path('<slug:slug>/add/', add_product, name='add'),
    path('<slug:slug>/order/', order_product, name='order'),
    path('<slug:slug>/delete/', delete_product, name='delete'),
]
