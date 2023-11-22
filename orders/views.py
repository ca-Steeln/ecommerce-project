
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import error, success
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse

from registration.models import CustomUser
from decorators.decorators import owner_only

from .settings import ABORTED, PAID, SHIPPED, CREATED, REFUNDED, STALE, PENDING, INVENTORY_ORDER
from .models import Order

# Create your views here.

@owner_only
def orders_view(request, pk=None):
    ctx = {}

    client = get_object_or_404(CustomUser, pk=pk)
    obj = Order.objects.filter(client=client)

    ctx['obj'], ctx['client'] = obj, client
    template = 'apps/orders/orders.html'
    return render(request, template, ctx)

@owner_only
def order_view(request, pk=None, slug=None):
    ctx = {}
    client = get_object_or_404(CustomUser, pk=pk)
    order = get_object_or_404(Order, client=client, slug=slug)
    qs = order.items.all()
    order_type = order.order_type == INVENTORY_ORDER

    ctx['order'], ctx['client'], ctx['qs'], ctx['order_type'] = order, client, qs, order_type
    template = 'apps/orders/order.html'
    return render(request, template, ctx)

@owner_only
def abort_order(request, pk=None, slug=None):
    ctx = {}

    client = get_object_or_404(CustomUser, pk=pk)
    obj = get_object_or_404(Order, client=client, slug=slug)

    if request.method == 'POST':
        if request.POST.get('orders:abort') is not None:

            if not any([obj.status == CREATED, obj.status == PENDING]):
                error(request, f'Order with status of \'{obj.get_status_display()}\' cannot be aborted')
                return HttpResponse(status=204)

            obj.status = ABORTED
            obj.save()
            success(request, 'Order has aborted successfully.')

            reverse_url = obj.get_absolute_url()
            if request.htmx:
                headers={
                    'HX-Location': reverse_url
                }
                return HttpResponse(f'{request.user.username} Aborted order {obj.get_absolute_url()}. at {obj.updated_at}.', headers=headers)
            return redirect(reverse_url)

        else:
            error(request, 'something went worng.')

    ctx['obj'] = obj
    template = 'apps/orders/abort.html'
    return render(request, template, ctx)