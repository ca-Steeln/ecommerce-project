
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import error, success
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.urls import reverse

from .settings import ABORTED, PAID, SHIPPED, CREATED, REFUNDED, STALE, PENDING, INVENTORY_ORDER
from .models import Order

# Create your views here.

def orders_view(request, client_pk=None, *args, **kwargs):
    ctx = {}

    if not request.user.pk == client_pk:
        raise Http404

    client = get_object_or_404(User, pk=client_pk, id=request.user.id)
    obj = Order.objects.filter(client=client)

    ctx['obj'], ctx['client'] = obj, client
    template = 'apps/orders/orders.html'
    return render(request, template, ctx)


def order_view(request, client_pk=None, slug=None, *args, **kwargs):
    ctx = {}

    if not request.user.pk == client_pk:
        raise Http404

    client = get_object_or_404(User, pk=client_pk, id=request.user.id)
    order = get_object_or_404(Order, client=client, slug=slug)

    qs = order.items.all()

    order_type = order.order_type == INVENTORY_ORDER

    ctx['order'], ctx['client'], ctx['qs'], ctx['order_type'] = order, client, qs, order_type
    template = 'apps/orders/order.html'
    return render(request, template, ctx)

# unfinished code need(template, view)
def abort_order(request, client_pk=None, slug=None, *args, **kwargs):
    ctx = {}

    if not request.user.pk == client_pk:
        raise Http404

    client = get_object_or_404(User, pk=client_pk, id=request.user.id)
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