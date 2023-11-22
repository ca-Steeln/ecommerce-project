
from django.shortcuts import render

# Create your views here.


def exception_404_view(request, exception):

    template = 'exceptions/404.html'
    return render(request, template, status=404)