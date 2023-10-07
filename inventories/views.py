
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import error, success, info
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.urls import reverse

from products.models import Product
from orders.models import Order
from .models import Inventory
# Create your views here.


@login_required
def inventory_view(request, client_pk=None, *args, **kwargs):
    ctx = {}

    if not request.user.pk == client_pk:
        raise Http404

    client = get_object_or_404(User, pk=client_pk, id=request.user.id)
    inventory = get_object_or_404(Inventory, client=client)
    products = inventory.products.all()

    ctx= {'obj': inventory, 'client':client, 'products':products}

    template = 'apps/inventories/inventory.html'
    return render(request, template, ctx)


def order_inventory(request, client_pk=None, *args, **kwargs):

    if not request.user.pk == client_pk:
        raise Http404

    client = get_object_or_404(User, pk=client_pk, id=request.user.id)
    inventory = get_object_or_404(Inventory, client=client)


    if request.method == 'POST':

        if request.POST.get('inventories:order') is not None:

            if inventory.products.count() <= 0:
                error(request, 'Inventory has no products to order.')


            elif request.POST.get('agreement') is None:
                error(request, 'Invalid argument.')
                return HttpResponse(status=200)


            elif client.order_set.filter(status='created').exists():
                error(request, 'Duplicate ordering detected, Recent order still in first state.')
                return HttpResponse(status=200)


            else:
                order = Order.objects.create(client=client)

                for product in inventory.products.all():
                    order.products.add(product)

                inventory.products.clear()

                success(request, 'Your order went successfully.')

                reverse_url = order.get_orders_url()
                if request.htmx:
                    headers={
                        'HX-Location': reverse_url
                    }
                    return HttpResponse(f'{request.user.username} Ordered his inventory {inventory.get_inventory_url()}.', headers=headers)
                return redirect(reverse_url)


    ctx= {'obj':inventory}

    template = 'apps/inventories/order.html'
    return render(request, template, ctx)


def delete_product(request, client_pk=None, product_slug=None, *args, **kwargs):

    if not request.user.pk == client_pk:
        raise Http404

    client = get_object_or_404(User, pk=client_pk, id=request.user.id, username=request.user.username)
    inventory = get_object_or_404(Inventory, client=client)
    products = inventory.products.filter(slug=product_slug)

    if not products.exists():
        error(request, 'Product does not exists in your inventory.')
        reverse_url = inventory.get_inventory_url()
        if request.htmx:
            headers={
                'HX-Location': reverse_url
            }
            return HttpResponse(f'Product does not exists in your inventory {inventory.get_inventory_url()}.', headers=headers)
        return redirect(reverse_url)

    product = products.first()

    if request.method == 'POST':

        if request.POST.get('inventories:delete') is not None:
            inventory.products.remove(product)
            success(request, 'Product has been deleted.')

            reverse_url = inventory.get_inventory_url()
            if request.htmx:
                headers={
                    'HX-Location': reverse_url
                }
                return HttpResponse(f'{request.user.username} Deleted product from his inventory {inventory.get_inventory_url()}.', headers=headers)
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
            if inventory.products.count() > 0:
                inventory.products.clear()

                success(request, 'Inventory has been cleared.')

                reverse_url = inventory.get_inventory_url()
                if request.htmx:
                    headers={
                        'HX-Location': reverse_url
                    }
                    return HttpResponse(f'{request.user.username} Aborted product from his inventory {inventory.get_inventory_url()}.', headers=headers)
                return redirect(reverse_url)
            else:
                error(request, 'Your inventory is already empty.')

    ctx= {'obj':inventory}

    template = 'apps/inventories/clear.html'
    return render(request, template, ctx)