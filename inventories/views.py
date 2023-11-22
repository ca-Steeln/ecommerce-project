
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import error, success, info
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse

from registration.models import CustomUser
from orders.models import Order
from orders.settings import INVENTORY_ORDER, CREATED
from decorators.decorators import owner_only

from .models import Inventory
from .forms import ProductItemForm

# Create your views here.


@owner_only
def inventory_view(request, pk=None):

    ctx = {}

    client = get_object_or_404(CustomUser, pk=pk)
    inventory = get_object_or_404(Inventory, client=client)
    items = inventory.items.all()

    ctx= {'obj': inventory, 'client':client, 'items':items}

    template = 'apps/inventories/inventory.html'
    return render(request, template, ctx)

@owner_only
def order_inventory(request, pk=None):

    client = get_object_or_404(CustomUser, pk=pk)
    inventory = get_object_or_404(Inventory, client=client)
    items = inventory.items
    if request.method == 'POST':

        form = ProductItemForm(request.POST)

        if request.POST.get('inventories:order') is not None:


            if form.errors:
                for k, e in form.errors.items():
                    error(request, e)

            # Order.by_user_pk.is_created().exists()
            elif client.order_set.filter(status=CREATED).exists():
                error(request, 'Duplicate ordering detected, Recent order still in first state.')
                return HttpResponse(status=200)

            elif form.is_valid():

                note = form.cleaned_data['note']

                order = Order.objects.create(client=client, order_type=INVENTORY_ORDER, note=note)
                total_amount, total_price = 0, 0
                for item in items.all():
                    order.items.add(item)
                    total_amount += item.amount
                    total_price += item.product.price * item.amount

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

    else:
        form = ProductItemForm()

    ctx= {'form':form, 'obj':inventory}

    template = 'apps/inventories/order.html'
    return render(request, template, ctx)

@owner_only
def delete_product(request, pk=None, product_slug=None):


    client = get_object_or_404(CustomUser, pk=pk)
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

@owner_only
def clear_inventory(request, pk=None):

    client = get_object_or_404(CustomUser, pk=pk)
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