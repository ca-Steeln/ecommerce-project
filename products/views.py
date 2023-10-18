
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import error, success, info
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.urls import reverse

from categories.models import Category
from inventories.models import Inventory
from orders.models import Order
from orders.settings import CREATED, PRODUCT_ORDER

from .models import Product, ProductItem
from .forms import CreateProductForm, UpdateProductForm, ProductItemForm

# Create your views here.


def products_view(request, category_name=None, *args, **kwargs):
    ctx = {}
    category = get_object_or_404(Category, name= category_name)
    qs = Product.objects.filter(active=True)


    ctx['qs'] = qs
    ctx['category'] = category
    template = 'apps/products/products.html'
    return render(request, template, ctx)

def product_view(request, category_name=None, slug=None, *args, **kwargs):

    category = get_object_or_404(Category, name= category_name)
    obj = get_object_or_404(Product, category=category, slug=slug, active=True)

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

                reverse_url = product.get_absolute_url()
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

                reverse_url = product.get_absolute_url()
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
@user_passes_test(lambda user: user.is_authenticated)
def order_product(request, category_name=None, slug=None, *args, **kwargs):

    category = get_object_or_404(Category, name= category_name)
    obj = get_object_or_404(Product, category=category, slug=slug, active=True)

    if request.method == 'POST':

        client = get_object_or_404(User, pk=request.user.pk, id=request.user.id)
        form = ProductItemForm(request.POST)

        if form.is_valid():

            # getting user inputs values from 'data form'.
            amount = form.cleaned_data['amount']
            notes = form.cleaned_data['notes']

            # case users ordered product dircetly.
            if request.POST.get('products:order'):

                if request.POST.get('agreement') is None:
                    error(request, 'Invalid argument.')
                    return HttpResponse(status=200)

                # note: make sure that if really u need to check that.
                # that were made to not override orders with same status and items or product.
                elif client.order_set.filter(status=CREATED).exists():
                    error(request, 'Duplicate ordering detected, Recent order still in first state \'New\'.')
                    return HttpResponse(status=200)

                else:
                    # more clean code needed here, has to be a better way to code this.

                    # Get or create Product Item
                    product_item, created = ProductItem.objects.get_or_create(product = obj, amount = amount)

                    unit_price = obj.price
                    total_price = unit_price * amount

                    # creating the order
                    order = Order.objects.create(
                        client=client, order_type=PRODUCT_ORDER, status=CREATED,
                        unit_price=unit_price, total_price=total_price,
                        total_amount=amount, notes=notes,
                        )

                    order.items.add(product_item)

                    success(request, 'Order has been created successfully.')

                    reverse_url = order.get_absolute_url()
                    if request.htmx:
                        headers={
                            'HX-Location': reverse_url
                        }
                        return HttpResponse(status=200, headers=headers)
                    return redirect(reverse_url)

            else:
                error(request, 'Something went worng.')
    else:
        form = ProductItemForm()

    ctx = {'obj':obj, 'form': form}
    template = 'apps/products/order.html'
    return render(request, template, ctx)

@login_required
@user_passes_test(lambda user: user.is_authenticated)
def add_product(request, category_name=None, slug=None, *args, **kwargs):

    category = get_object_or_404(Category, name= category_name)
    obj = get_object_or_404(Product, category=category, slug=slug, active=True)

    if request.method == 'POST':

        if request.user.is_anonymous:
            error(request, 'Login required.')
            return HttpResponse(status=200)

        client = get_object_or_404(User, pk=request.user.pk, id=request.user.id)
        form = ProductItemForm(request.POST)

        if form.is_valid():

            # getting user inputs values from 'data form'.
            amount = form.cleaned_data['amount']

            # case users added product in thier inventory.
            if request.POST.get('products:add'):

                # checking user inventory & inventory products.
                inventory = get_object_or_404(Inventory, client=client)
                if inventory.items.filter(product = obj).exists():
                    error(request, 'You already have that product in your inventory.')
                    return HttpResponse(status=200)


                # getting or creating items similar to user request
                product_item, created = ProductItem.objects.get_or_create(product = obj, amount = amount)

                # add the items that user order to his inventory
                inventory.items.add(product_item)
                success(request, 'Product has been added to your inventory.')

                reverse_url = category.get_absolute_url()
                if request.htmx:
                    headers={
                        'HX-Location': reverse_url
                    }
                    return HttpResponse(f'{request.user.username} Ordered his inventory {inventory.get_absolute_url()}.', headers=headers)
                return redirect(reverse_url)

            else:
                error(request, 'Something went worng.')
    else:
        form = ProductItemForm()

    ctx = {'obj':obj, 'form': form}
    template = 'apps/products/add.html'
    return render(request, template, ctx)

@login_required
@user_passes_test(lambda user: user.is_staff)
def delete_product(request, category_name=None, slug=None, *args, **kwargs):

    ctx = {}

    category = get_object_or_404(Category, name= category_name)
    obj = get_object_or_404(Product, category=category, slug=slug)

    if not obj.active:
        info(request, 'Product is not active.')

    if request.method == 'POST':
        if not request.user.is_staff:
            raise Http404

        if request.POST.get('products:delete') is not None:
            obj.delete()
            success(request, f'Product \'{obj.name}\' has been deleted.')
            reverse_url = category.get_absolute_url()
            if request.htmx:
                headers={
                        'HX-Location': reverse_url
                    }
                return HttpResponse(f'{request.user.username} Deleted Product named {obj.name or obj.title}.', headers=headers)
            return redirect(reverse_url)

    ctx['obj'] = obj
    template = 'apps/products/delete.html'
    return render(request, template, ctx)