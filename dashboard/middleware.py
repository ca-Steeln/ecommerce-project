
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import get_object_or_404
from django.contrib.messages import get_messages, error, success
from django.http import HttpResponseForbidden, Http404
from django.urls import resolve

from registration.models import CustomUser
from project.settings import ACTIVE_USER, ADMIN_ROLE, MANAGER_GROUP, MANAGER_ROLE

from .urls import app_name


class MiddlewarePermissions(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        app_name_space = resolve(request.path_info).namespaces
        if app_name_space == [app_name]:
            user = get_object_or_404(CustomUser, pk= request.user.pk, is_manager=True, status=ACTIVE_USER)
            if not (user.role == MANAGER_ROLE or user.role == ADMIN_ROLE) or not (user.groups.filter(name=MANAGER_GROUP).exists()):
                # report moderation
                print(f'Report {user} - {user.id}')
                raise Http404
        return self.get_response(request)

