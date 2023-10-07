
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.messages import success, error
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test


from .forms import RegisterForm, LoginForm

# Create your views here.

def register_form_view(request):
    ctx = {}

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if request.POST.get('registration:sign-up') is not None:
            if form.errors:
                for k, e in form.errors.items():
                    error(request, e)

            elif form.is_valid():
                user = form.save()
                ctx['form'] = RegisterForm()
                login(request, user)

                success(request, 'You have successfully logged in.')

                reverse_url = reverse('pages:home')
                if request.htmx:
                    headers={
                        'HX-Location': reverse_url
                    }
                    return HttpResponse(f'{user.username} signed up.', headers=headers)

    else:
        form = RegisterForm()

    ctx['form'] = form
    template = 'apps/registration/sign-up.html'
    return render(request, template, ctx)


@user_passes_test(lambda user: user.is_anonymous)
def login_form_view(request):
    ctx = {}

    if request.method == 'POST':

        if request.POST.get('registration:login')is not None:
            form = LoginForm(request, data=request.POST)

            if form.errors:
                for k, e in form.errors.items():
                    error(request, e)

            elif form.is_valid():
                ctx['form'] = LoginForm()
                user = form.get_user()
                login(request, user)

                success(request, 'You have successfully logged in.')

                reverse_url = reverse('pages:home')
                if request.htmx:
                    headers={
                        'HX-Location': reverse_url
                    }
                    return HttpResponse(f'{user.username} logged in.', headers=headers)
                return redirect(reverse_url)


        else:
            error(request, 'Something went wrong :(')
    else:
        form = LoginForm()

    ctx['form'] = form
    template = 'apps/registration/login.html'
    # if request.htmx:
    #     template = 'apps/registration/forms/login.html'
    return render(request, template, ctx)

@login_required(login_url= '/login')
@user_passes_test(lambda user: user.is_authenticated)
def logout_form_view(request):
    ctx = {}

    if request.method == 'POST':
        if request.POST.get('registration:logout'):
            user = request.user
            logout(request)

            reverse_url = reverse('registration:sign-up')
            if request.htmx:
                headers={
                    'HX-Location': reverse_url
                }
                return HttpResponse(f'{user.username} logged out.', headers=headers)
            return redirect(reverse_url)

    template = 'apps/registration/logout.html'
    return render(request, template, ctx)

