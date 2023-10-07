
from django.urls import path

from .views import (
    products_view, create_product ,product_view , update_product, delete_product
    )

app_name = 'products'

urlpatterns = [
    path('', products_view, name='products'),
    path('create/', create_product, name='create'),
    path('<slug:slug>/', product_view, name='product'),
    path('<slug:slug>/update/', update_product, name='update'),
    path('<slug:slug>/delete/', delete_product, name='delete'),

]
