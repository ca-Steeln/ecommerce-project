
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import error, success, info
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.urls import reverse

from products.models import  Product
from orders.models import Order
from orders.settings import INVENTORY_ORDER, CREATED

from .models import Inventory
# Create your views here.


@login_required
def inventory_view(request, client_pk=None, *args, **kwargs):
    ctx = {}

    if not request.user.pk == client_pk:
        raise Http404

    client = get_object_or_404(User, pk=client_pk, id=request.user.id)
    inventory = get_object_or_404(Inventory, client=client)
    items = inventory.items.all()

    ctx= {'obj': inventory, 'client':client, 'items':items}

    template = 'apps/inventories/inventory.html'
    return render(request, template, ctx)


def order_inventory(request, client_pk=None, *args, **kwargs):

    if not request.user.pk == client_pk:
        raise Http404

    client = get_object_or_404(User, pk=client_pk, id=request.user.id)
    inventory = get_object_or_404(Inventory, client=client)
    items = inventory.items
    if request.method == 'POST':

        if request.POST.get('inventories:order') is not None:

            if items.count() <= 0:
                error(request, 'Inventory has no products to order.')
                return HttpResponse(status=200)

            elif request.POST.get('agreement') is None:
                error(request, 'Invalid argument.')
                return HttpResponse(status=200)

            # note: make sure that if really u need to check that.
            # that were made to not override orders with same status and items or products.
            elif client.order_set.filter(status=CREATED).exists():
                error(request, 'Duplicate ordering detected, Recent order still in first state.')
                return HttpResponse(status=200)

            else:
                order = Order.objects.create(
                    client=client, order_type=INVENTORY_ORDER, status=CREATED,
                    )

                total_amount, total_price = 0, 0

                for item in items.all():
                    order.items.add(item)
                    total_amount += item.amount
                    total_price += item.product.price

                order.total_amount = total_amount
                order.total_price = total_price
                order.save()

                items.clear()

                success(request, 'Order has been created successfully.')

                reverse_url = order.get_absolute_url()
                if request.htmx:
                    headers={
                        'HX-Location': reverse_url
                    }
                    return HttpResponse(status=200, headers=headers)
                return redirect(reverse_url)


    ctx= {'obj':inventory}

    template = 'apps/inventories/order.html'
    return render(request, template, ctx)


def delete_product(request, client_pk=None, product_slug=None, *args, **kwargs):

    if not request.user.pk == client_pk:
        raise Http404

    client = get_object_or_404(User, pk=client_pk, id=request.user.id, username=request.user.username)
    inventory = get_object_or_404(Inventory, client=client)

    # get the product to remove from client invetory !!!
    product = inventory.items.filter(product__slug = product_slug)

    if not product.exists():
        error(request, 'Product does not exists in your inventory.')
        reverse_url = inventory.get_absolute_url()
        if request.htmx:
            headers={
                'HX-Location': reverse_url
            }
            return HttpResponse(f'Product does not exists in your inventory {inventory.get_absolute_url()}.', headers=headers)
        return redirect(reverse_url)

    product = product.first()

    if request.method == 'POST':

        if request.POST.get('inventories:delete') is not None:
            inventory.items.remove(product)
            success(request, 'Product has been deleted.')

            reverse_url = inventory.get_absolute_url()
            if request.htmx:
                headers={
                    'HX-Location': reverse_url
                }
                return HttpResponse(f'{request.user.username} Deleted product from his inventory.', headers=headers)
            return redirect(reverse_url)


    ctx= {'obj':product, 'inventory':inventory}

    template = 'apps/inventories/delete.html'
    return render(request, template, ctx)


def clear_inventory(request, client_pk=None, *args, **kwargs):

    if not request.user.pk == client_pk:
        raise Http404

    client = get_object_or_404(User, pk=client_pk, id=request.user.id, username=request.user.username)
    inventory = get_object_or_404(Inventory, client=client)

    if request.method == 'POST':
        if request.POST.get('inventories:clear') is not None:
            if inventory.items.count() > 0:
                inventory.items.clear()
                success(request, 'Inventory has been cleared.')

            else:
                error(request, 'Your inventory is already empty.')

            reverse_url = inventory.get_absolute_url()
            if request.htmx:
                headers={
                    'HX-Location': reverse_url
                }
                return HttpResponse(f'{request.user.username} Aborted product from his inventory {inventory.get_absolute_url()}.', headers=headers)
            return redirect(reverse_url)

    ctx= {'obj':inventory}

    template = 'apps/inventories/clear.html'
    return render(request, template, ctx)