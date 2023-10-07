
from django.urls import path

from .views import (
    categories_view, create_category ,category_view , update_category, delete_category
    )

app_name = 'categories'

urlpatterns = [
    path('', categories_view, name='categories'),
    path('create/', create_category, name='create'),
    path('<str:name>/', category_view, name='category'),
    path('<str:name>/update/', update_category, name='update'),
    path('<str:name>/delete/', delete_category, name='delete'),

]
