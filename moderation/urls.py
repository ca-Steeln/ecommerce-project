
from django.urls import path

from .views import moderation_view

app_name = 'moderation'

urlpatterns = [
    # view paths
    path('', moderation_view, name='moderation'),

]
