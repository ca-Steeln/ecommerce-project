
from django.urls import path
from .consumers import DashboardConsumer, DashboardUsersConsumer, DashboardUserConsumer

websocket_urlpatterns = [
    path('ws/dashboard/', DashboardConsumer.as_asgi()),
    path('ws/dashboard/users/', DashboardUsersConsumer.as_asgi()),
    path('ws/dashboard/users/<str:pk>/', DashboardUserConsumer.as_asgi()),
]