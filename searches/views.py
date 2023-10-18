
from django.http import HttpResponse
from django.shortcuts import render

from .models import Search

from categories.models import Category
from products.models import Product

# Create your views here.

SEARCH_TYPE_MAPPING = {

    'categories': Category,
    'products': Product
}

def search_view(request):
    ctx={}

    query = request.GET.get('q')

    if query:
        search_type = request.GET.get('type')

        if search_type in SEARCH_TYPE_MAPPING.keys():
            klass = SEARCH_TYPE_MAPPING[search_type]
            qs = klass.objects.search(query=query)
            ctx[f'{search_type}_qs'] = qs

        else:
            for search_type, klass in SEARCH_TYPE_MAPPING.items():
                ctx[f'{search_type}_qs'] = klass.objects.search(query=query)


    template = 'apps/searches/results.html'
    return render(request, template, ctx)
