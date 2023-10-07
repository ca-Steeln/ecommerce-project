
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error, success
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate

from .models import Account
from .forms import AccountForm, UserForm


# Create your views here.

def account_view(request, pk=None):
    ctx = {}
    obj = get_object_or_404(User, pk=pk)
    ctx['obj'] = obj

    template = 'apps/accounts/account.html'
    if request.htmx:
        if not request.method == "GET":
            template = 'apps/accounts/forms/account.html'
    return render(request, template, ctx)

def edit_account_view(request, pk=None):
    ctx = {}

    if not request.user.pk == pk:
        raise Http404

    obj = get_object_or_404(User, pk=pk, id=request.user.id)

    if request.method == 'POST':

        if request.POST.get('accounts:edit') is not None:
            u_form = UserForm(instance=obj)
            a_form = AccountForm(request.POST, instance=obj.account)

            if a_form.errors:
                for k, e in a_form.errors.items():
                    error(request, e)
                return HttpResponse(status=200)

            elif a_form.is_valid():

                password = request.POST.get('password')
                if authenticate(request, username=obj.username, password=password, id=id, pk=pk) is None:
                    error(request, 'Incorrect password.')
                    return HttpResponse(status=200)

                a_form.save(commit=False)
                a_form.user = obj
                a_form.save()

                success(request, 'Data changes have been saved.')

                if request.htmx:
                    headers={
                        'HX-Redirect': obj.get_account_url()
                    }
                    return HttpResponse(status=204, headers=headers)
                return redirect(obj.get_account_url())


            else:
                error(request, 'Something went wrong :(')

    else:
        u_form = UserForm(instance=obj)
        a_form = AccountForm(instance=obj.account)

    ctx['u_form'] = u_form
    ctx['a_form'] = a_form
    ctx['obj'] = obj

    template = 'apps/accounts/edit-account.html'
    # if request.htmx:
    #     template = 'apps/accounts/forms/edit-account.html'
    return render(request, template, ctx)