
from django.urls import path

from .views import products_view, product_view , add_product, order_product

app_name = 'products'

urlpatterns = [
    path('', products_view, name='products'),
    path('<slug:slug>/', product_view, name='product'),
    path('<slug:slug>/add/', add_product, name='add'),
    path('<slug:slug>/order/', order_product, name='order'),
]
