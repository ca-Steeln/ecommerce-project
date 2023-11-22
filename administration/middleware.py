
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import get_object_or_404
from django.contrib.messages import get_messages, error, success
from django.http import HttpResponseForbidden, Http404
from django.urls import resolve

from registration.models import CustomUser
from project.settings import ADMIN_GROUP, ACTIVE_USER, ADMIN_ROLE
from .urls import app_name


class MiddlewarePermissions(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        app_name_space = resolve(request.path_info).namespaces

        if app_name_space == [app_name]:
            user = get_object_or_404(CustomUser, pk= request.user.pk, is_staff=True, status=ACTIVE_USER, role=ADMIN_ROLE)
            if not user.groups.filter(name=ADMIN_GROUP).exists():
                # report administration
                print(f'Report {user} - {user.id}')
                raise Http404

        return self.get_response(request)



