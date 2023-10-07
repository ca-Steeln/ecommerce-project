
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import error, success, info
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.urls import reverse

from categories.models import Category
from inventories.models import Inventory

from .models import Product
from .forms import CreateProductForm, UpdateProductForm

# Create your views here.


def products_view(request, category_name=None, *args, **kwargs):
    ctx = {}
    category = get_object_or_404(Category, name= category_name)
    products = Product.objects.filter(active=True)


    ctx['obj'] = products
    ctx['category'] = category
    template = 'apps/products/products.html'
    return render(request, template, ctx)


def product_view(request, category_name=None, slug=None, *args, **kwargs):

    category = get_object_or_404(Category, name= category_name)
    obj = get_object_or_404(Product, category=category, slug=slug, active=True)

    if request.method == 'POST':

        if request.user.is_anonymous:
            error(request, 'Login required.')
            return HttpResponse(status=200)

        client = User.objects.get(pk=request.user.pk, id=request.user.id)

        if request.POST.get('products:add'):

            inventory = get_object_or_404(Inventory, client=client)
            if inventory.products.filter(slug = obj.slug).exists():
                error(request, 'You already have that product in your inventory.')

            else:
                inventory.products.add(obj)
                success(request, 'Product has been added to your inventory.')

                reverse_url = category.get_category_url()
                if request.htmx:
                    headers={
                        'HX-Location': reverse_url
                    }
                    return HttpResponse(f'{request.user.username} Ordered his inventory {inventory.get_inventory_url()}.', headers=headers)
                return redirect(reverse_url)


    ctx = {'obj':obj}
    template = 'apps/products/product.html'
    return render(request, template, ctx)


@login_required
@user_passes_test(lambda user: user.is_staff)
def create_product(request, category_name=None, *args, **kwargs):
    ctx = {}
    category = get_object_or_404(Category, name= category_name)

    if request.method == 'POST':

        if request.POST.get('products:create') is not None:
            form = CreateProductForm(request.POST, request.FILES)

            if form.errors:
                for k, e in form.errors.items():
                    error(request, e)

            elif form.is_valid():

                product = form.save(commit=False)
                product.author = request.user
                product.save()
                ctx['obj'] = product

                reverse_url = product.get_product_url()
                if request.htmx:
                    headers={
                        'HX-Location': reverse_url
                    }
                    return HttpResponse(f'{request.user.username} Created product named {product.name or product.title}.', headers=headers)
                return redirect(reverse_url)

            else:
                error(request, 'Something went wrong (.')
    else:
        form = CreateProductForm(initial={'category':category})

    ctx['form'] = form
    ctx['category'] = category
    template = 'apps/products/create.html'
    return render(request, template, ctx)

@login_required
@user_passes_test(lambda user: user.is_staff)
def update_product(request, category_name=None, slug=None, *args, **kwargs):
    ctx = {}

    category = get_object_or_404(Category, name= category_name)
    obj = get_object_or_404(Product,category=category, slug=slug)

    if request.method == 'POST':

        if request.POST.get('products:update') is not None:
            form = UpdateProductForm(request.POST, request.FILES, instance=obj)

            if form.errors:
                for k, e in form.errors.items():
                    error(request, e)

            elif form.is_valid():
                product = form.save(commit=False)
                product.author = request.user
                product.save()
                ctx['obj'] = product

                reverse_url = product.get_product_url()
                if request.htmx:
                    headers={
                        'HX-Location': reverse_url
                    }
                    return HttpResponse(f'{request.user.username} Updated Product named {obj.name or obj.title}.', headers=headers)
                return redirect(reverse_url)

            else:
                error(request, 'Something went wrong :(')


    else:
        form = UpdateProductForm(instance= obj)

    ctx['form'] = form
    ctx['obj'] = obj

    template = 'apps/products/update.html'
    return render(request, template, ctx)

@login_required
@user_passes_test(lambda user: user.is_staff)
def delete_product(request, category_name=None, slug=None, *args, **kwargs):

    ctx = {}

    category = get_object_or_404(Category, name= category_name)
    obj = get_object_or_404(Product, category=category, slug=slug)

    if not obj.active:
        info(request, 'Product is not available.')

    if request.method == 'POST':

        if not request.user.is_staff:
            raise Http404

        # add that on ur template
        elif request.POST.get('products:delete') is not None:
            obj.delete()

            reverse_url = obj.get_product_url()
            if request.htmx:
                headers={
                        'HX-Location': reverse_url
                    }
                return HttpResponse(f'{request.user.username} Deleted Product named {obj.name or obj.title}.', headers=headers)
            return redirect(reverse_url)

    ctx['obj'] = obj
    template = 'apps/products/delete.html'
    return render(request, template, ctx)