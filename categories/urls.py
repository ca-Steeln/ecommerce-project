
from django.urls import path

from .views import (
    categories_view, create_category ,category_view , update_category, delete_category
    )

app_name = 'categories'

urlpatterns = [
    path('', categories_view, name='categories'),
    path('create/', create_category, name='create'),
    path('<slug:slug>/', category_view, name='category'),
    path('<slug:slug>/update/', update_category, name='update'),
    path('<slug:slug>/delete/', delete_category, name='delete'),

]
