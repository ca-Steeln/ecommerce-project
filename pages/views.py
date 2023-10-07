
from django.shortcuts import render
from django.contrib.messages import success, error


# Create your views here.

def home_view(request):
    ctx = {'form':'success'}

    message = request.POST.get('message')
    if message is not None:
        success(request, 'Greetings')

    template = 'apps/pages/home.html'
    return render(request, template, ctx)


def about_view(request):
    ctx = {'form':'success'}

    template = 'apps/pages/about.html'
    return render(request, template, ctx)
