
from django.urls import path
from .views import dashboard_view, users_dashboard, users_chart, user_dashboard, products_dashboard, orders_dashboard, categories_dashboard

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('users/', users_dashboard, name='users'),
    path('users/chart/', users_chart, name='users_chart'),
    path('users/<str:pk>/', user_dashboard, name='user'),
    path('products/', products_dashboard, name='products'),
    path('orders/', orders_dashboard, name='orders'),
    path('categories/', categories_dashboard, name='categories'),
]
