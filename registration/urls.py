
from django.urls import path
from .views import register_form_view, login_form_view, logout_form_view

app_name = 'registration'

urlpatterns = [
    path('sign-up/', register_form_view, name='sign-up'),
    path('login/', login_form_view, name='login'),
    path('logout/', logout_form_view, name='logout')
]