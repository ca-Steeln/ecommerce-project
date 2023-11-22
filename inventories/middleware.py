
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import get_object_or_404
from django.contrib.messages import get_messages, error, success
from django.http import  Http404
from django.urls import resolve

from registration.models import CustomUser
from project.settings import CLIENT_GROUP, ACTIVE_USER
from inventories.models import Inventory

from .urls import app_name


class MiddlewarePermissions(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        app_name_space = resolve(request.path_info).namespaces

        if app_name_space == [app_name]:
            pk = resolve(request.path_info).kwargs['pk']
            user = get_object_or_404(CustomUser, pk=pk, status=ACTIVE_USER)

            if any([not user.groups.filter(name=CLIENT_GROUP).exists()]):
                # report administration
                print(f'Report {user} - {user.id}')
                raise Http404


        return self.get_response(request)



