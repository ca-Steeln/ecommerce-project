
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.messages import success, error
from django.urls import reverse

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
