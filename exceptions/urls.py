
from django.urls import path

from .views import exception_404_view

app_name = 'exceptions'

urlpatterns = [
    path('404', exception_404_view, name='404'),
]
