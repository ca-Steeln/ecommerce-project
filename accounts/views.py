
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import error, success
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate

from decorators.decorators import owner_only
from registration.models import CustomUser

from .forms import AccountForm, UserForm
from .models import Account


# Create your views here.

@owner_only
def account_view(request, pk=None):
    obj = get_object_or_404(CustomUser, pk=pk)
    ctx = {'obj':obj}
    template = 'apps/accounts/account.html'
    return render(request, template, ctx)


@owner_only
def edit_account_view(request, pk=None):

    ctx = {}

    obj = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':

        if request.POST.get('accounts:edit') is not None:
            user_form = UserForm(instance=obj)
            account_form = AccountForm(request.POST, instance=obj.account)


            if account_form.errors:
                for k, e in account_form.errors.items():
                    error(request, e)
                return HttpResponse(status=200)


            elif account_form.is_valid():

                password = account_form.cleaned_data['password']
                phone_obj = Account.objects.filter(phone=account_form.cleaned_data['phone'])
                if phone_obj.exists() and not phone_obj.first().user == obj:
                    error(request, 'Phone number must be unique.')

                elif not authenticate(request, username=obj.username, password=password, email=request.user.email, pk=pk, id=request.user.id) == obj:
                    error(request, 'Invalid Password.')

                else:
                    account_form.save(commit=False)
                    account_form.user = obj
                    account_form.save()

                    success(request, 'Data changes have been saved.')

                    if request.htmx:
                        headers={
                            'HX-Redirect': obj.account.get_absolute_url()
                        }
                        return HttpResponse(status=204, headers=headers)
                    return redirect(obj.get_account_url())


            else:
                error(request, 'Something went wrong :(')

    else:
        user_form = UserForm(instance=obj)
        account_form = AccountForm(instance=obj.account)

    ctx['u_form'] = user_form
    ctx['a_form'] = account_form
    ctx['obj'] = obj

    template = 'apps/accounts/edit-account.html'
    # if request.htmx:
    #     template = 'apps/accounts/forms/edit-account.html'
    return render(request, template, ctx)