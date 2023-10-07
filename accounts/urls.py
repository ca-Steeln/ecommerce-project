
from django.urls import path

from .views import account_view, edit_account_view

app_name = 'accounts'

urlpatterns = [
    path('<int:pk>/', account_view , name='account'),
    path('<int:pk>/edit/', edit_account_view , name='edit')
]
