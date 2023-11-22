
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import error, success, info
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse

from registration.models import CustomUser
from categories.models import Category
from inventories.models import Inventory
from orders.models import Order
from orders.settings import CREATED, PRODUCT_ORDER
from decorators.decorators import group_required, admin_only
from project.settings import CLIENT_GROUP

from .models import Product, ProductItem
from .forms import AddProductItemForm, OrderProductItemForm

# Create your views here.


def products_view(request):

    qs = Product.objects.filter(active=True)
    ctx = {'qs':qs}
    template = 'apps/products/products.html'
    return render(request, template, ctx)

def product_view(request,  slug=None):

    obj = get_object_or_404(Product, slug=slug, active=True)

    ctx = {'obj':obj}
    template = 'apps/products/product.html'
    return render(request, template, ctx)

@group_required(CLIENT_GROUP)
def order_product(request, slug=None):


    obj = get_object_or_404(Product, slug=slug, active=True)

    if request.method == 'POST':

        client = get_object_or_404(CustomUser, pk=request.user.pk, id=request.user.id)
        form = OrderProductItemForm(request.POST)

        if request.POST.get('products:order'):

            if client.order_set.filter(status=CREATED).exists():
                error(request, 'Duplicate ordering detected, Recent order still in first status.')
                return HttpResponse(status=200)

            elif form.is_valid():

                # getting user inputs values from 'data form'.
                note = form.cleaned_data['note']
                amount = form.cleaned_data['amount']

                # Get or create Product Item
                product_item, created = ProductItem.objects.get_or_create(product = obj, amount = amount)

                # creating the order
                order = Order.objects.create(
                    client=client, order_type=PRODUCT_ORDER, total_amount=amount, note=note
                )

                order.unit_price, order.total_price = obj.price, obj.price * amount
                order.items.add(product_item)
                order.save()

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
        form = OrderProductItemForm()

    ctx = {'obj':obj, 'form': form}
    template = 'apps/products/order.html'
    return render(request, template, ctx)

@group_required(CLIENT_GROUP)
def add_product(request, slug=None):

    obj = get_object_or_404(Product, slug=slug, active=True)

    if request.method == 'POST':

        client = get_object_or_404(CustomUser, pk=request.user.pk, id=request.user.id)
        form = AddProductItemForm(request.POST)

        if request.POST.get('products:add'):

            if form.is_valid():

                # getting user inputs values from 'data form'.
                note = form.cleaned_data['note']
                amount = form.cleaned_data['amount']

                # checking user inventory & inventory products.
                inventory = get_object_or_404(Inventory, client=client)
                if inventory.items.filter(product = obj).exists():
                    error(request, 'You already have that product in your inventory.')
                    return HttpResponse(status=200)


                # getting or creating items similar to user request
                product_item, created = ProductItem.objects.get_or_create( product = obj, amount = amount)

                # add the items that user order to his inventory
                inventory.items.add(product_item)
                success(request, 'Product has been added to your inventory.')

            else:
                error(request, 'Something went worng.')
    else:
        form = AddProductItemForm()

    ctx = {'obj':obj, 'form': form}
    template = 'apps/products/add.html'
    return render(request, template, ctx)
