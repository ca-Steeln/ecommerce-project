
from django.urls import path

from .views import search_view


app_name = 'searches'

urlpatterns = [
    path('', search_view, name='search'),
]
