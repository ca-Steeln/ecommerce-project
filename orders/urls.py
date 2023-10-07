
from django.urls import path
from .views import order_view, orders_view, abort_order

app_name = 'orders'

urlpatterns = [
    path('', orders_view, name='orders'),
    path('<slug:slug>/', order_view, name='order'),
    path('<slug:slug>/abort/', abort_order, name='abort'),
]