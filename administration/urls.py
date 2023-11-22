
from django.urls import path

from .views import (
    administration_view,
    users_view, user_management, set_banned, set_default, set_mod, set_manager,
    account_management,
    products_view, product_management, create_product, delete_product,
    categories_view, category_management, create_category, delete_category,
    orders_view, order_management, delete_order, client_orders_view
    )

app_name = 'administration'


urlpatterns = [
    # security :
    # change this route "administration/" in production
    path('', administration_view, name='administration'),

    # CustomUser
    path('users/', users_view , name='users'),
    path('users/<int:pk>/management/', user_management , name='user'),
    path('users/<int:pk>/ban/', set_banned, name='set-banned'),
    path('users/<int:pk>/default/', set_default, name='set-default'),
    path('users/<int:pk>/moderator/', set_mod, name='set-mod'),
    path('users/<int:pk>/manager/', set_manager, name='set-manager'),


    # Account
    path('accounts/<int:pk>/management/', account_management , name='account'),

    # Product
    path('products/', products_view , name='products'),
    path('products/<slug:slug>/management/', product_management , name='product'),
    path('products/create/', create_product, name='product-create'),
    path('products/<slug:slug>/delete/', delete_product, name='product-delete'),

    # Category
    path('categories/', categories_view , name='categories'),
    path('categories/<slug:slug>/management/', category_management , name='category'),
    path('categories/create/', create_category, name='category-create'),
    path('categories/<slug:slug>/delete/', delete_category, name='category-delete'),

    # Order
    path('orders/', orders_view , name='orders'),
    path('orders/client/<int:client_pk>', client_orders_view , name='client-orders'),
    path('orders/<slug:slug>/management/', order_management , name='order'),
    path('orders/<slug:slug>/delete/', delete_order, name='order-delete'),

]


