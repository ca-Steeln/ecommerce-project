
from django.shortcuts import get_object_or_404
from django.contrib.messages import error, success
from django.http import HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from functools import wraps
from registration.models import CustomUser

from project.settings import MOD_GROUP, ACTIVE_USER, MOD_ROLE, ADMIN_ROLE, ADMIN_GROUP, CLIENT_GROUP, MANAGER_ROLE, MANAGER_GROUP

def admin_only(view):

    @wraps(view)
    @login_required
    def wrapped_view(request, *args, **kwargs):
        user = request.user
        obj = get_object_or_404(CustomUser, pk=user.pk, id= user.id, is_staff=True, status=ACTIVE_USER, role=ADMIN_ROLE)
        if not obj.groups.filter(name=ADMIN_GROUP).exists():
            raise Http404

        return view(request, *args, **kwargs)

    return wrapped_view


def moderator_required(view):

    @wraps(view)
    @login_required
    def wrapped_view(request, *args, **kwargs):

        user = get_object_or_404(CustomUser, pk=request.user.pk, is_mod=True, status=ACTIVE_USER)
        if not (user.role == MOD_ROLE or user.role == ADMIN_ROLE) or not (user.groups.filter(name=MOD_GROUP).exists()):
            # report administration
            print(f'Report {user} - {user.id}')
            raise Http404

        return view(request, *args, **kwargs)

    return wrapped_view


def manager_required(view):

    @wraps(view)
    @login_required
    def wrapped_view(request, *args, **kwargs):

        user = get_object_or_404(CustomUser, pk=request.user.pk, is_manager=True, status=ACTIVE_USER)
        if not (user.role == MANAGER_ROLE or user.role == ADMIN_ROLE) or not (user.groups.filter(name=MANAGER_GROUP).exists()):
            # report moderation
            print(f'Report {user} - {user.id}')
            raise Http404
        return view(request, *args, **kwargs)
    return wrapped_view


def group_required(group_name:str):

    def decorator(view):

        @wraps(view)
        @login_required(login_url='login/')
        def wrapped_view(request, *args, **kwargs):

            if not request.user.groups.filter(name=group_name).exists():
                return HttpResponseForbidden
            return view(request, *args, **kwargs)
        return wrapped_view

    return decorator


def owner_only(view, model=CustomUser):

    @wraps(view)
    @login_required
    def wrapped_view(request, *args, **kwargs):
        pk = kwargs['pk']
        user = get_object_or_404(model, pk=pk, status=ACTIVE_USER)
        if not request.user.is_staff and any([not user == request.user, not user.groups.filter(name=CLIENT_GROUP).exists()]):
            raise Http404

        return view(request, *args, **kwargs)
    return wrapped_view


def anonymous_only(view):

    @wraps(view)
    def wrapped_view(request, *args, **kwargs):

        if request.user.is_anonymous:
            return view(request, *args, **kwargs)

        else:
            raise HttpResponseForbidden

    return wrapped_view


# # Beta
# def allow_status_only(status:str, group_name:str):

#     def decorator(view):

#         @wraps(view)
#         @login_required
#         def wrapped_view(request, *args, **kwargs):

#             user = request.user
#             if user.status == status and user.groups.filter(name=group_name).exists():
#                 return view(request, *args, **kwargs)

#             else:
#                 return HttpResponseForbidden("Permission denied")

#         return wrapped_view

#     return decorator

# # Beta
# def reject_status_only(status:str, group_name:str):

#     def decorator(view):

#         @wraps(view)
#         @login_required
#         def wrapped_view(request, *args, **kwargs):
#             user = request.user
#             if user.status == status or user.groups.filter(name=group_name).exists():
#                 return HttpResponseForbidden("Permission denied")

#             else:
#                 return view(request, *args, **kwargs)


#         return wrapped_view

#     return decorator