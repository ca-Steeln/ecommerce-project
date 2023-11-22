from channels.db import database_sync_to_async

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group
from django.http import Http404, HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.db.models import Sum

# Models
from registration.models import CustomUser
from products.models import Product
from orders.models import Order
from categories.models import Category

from project.settings import (
    USER_GROUPS_CHOICES, USER_STATUS_CHOICES, USER_ROLES_CHOICES,
    BANNED_GROUP, CLIENT_GROUP, MOD_GROUP,
    ACTIVE_USER, BANNED_USER, DELETED_USER,
    DEFAULT_ROLE, MOD_ROLE, MANAGER_ROLE, ADMIN_ROLE
    )
from decorators.decorators import admin_only, manager_required

from .utils import calc_percentage

# Create your views here.

@manager_required
def dashboard_view(request):
    ctx = {}
    template = 'apps/dashboard/dashboard.html'
    return render(request, template, ctx)


@manager_required
def users_dashboard(request):

    qs = CustomUser.objects.all()
    qs_count = qs.count()

    data = {
        #'search_result': CustomUser.objects.search(1)

        'qs': qs,
        'qs_count': qs_count,
    }
    template = 'apps/dashboard/customuser/users.html'
    return render(request, template, data)

@manager_required
def users_chart(request):

    qs = CustomUser.objects.all()

    status_chart_labels = [ACTIVE_USER, BANNED_USER, DELETED_USER]
    status_chart_data = [qs.active(True), qs.banned(True), qs.deleted(True)]

    roles_chart_labels = [DEFAULT_ROLE, MOD_ROLE, MANAGER_ROLE, ADMIN_ROLE]
    roles_chart_data = [qs.default(True), qs.mod(True), qs.manager(True), qs.admin(True)]

    data = {
        'statusChartLabels': status_chart_labels,
        'statusChartData': status_chart_data,

        'rolesChartLabels': roles_chart_labels,
        'rolesChartData': roles_chart_data,
    }

    return JsonResponse(data)

@manager_required
def user_dashboard(request, pk):

    obj = get_object_or_404(CustomUser, pk=pk)

    # calc last order
    data = {
        'obj': obj,
    }

    template = 'apps/dashboard/customuser/user.html'
    return render(request, template, data)

@manager_required
def products_dashboard(request):

    qs = Product.objects.all()

    data = {
        'qs': qs,
        'qs_count': qs.count(),
    }

    template = 'apps/dashboard/product/products.html'
    return render(request, template, data)

@manager_required
def orders_dashboard(request):
    qs = Order.objects.all()

    data = {

        'qs_count': qs.count(),

        'qs_inventory_type': qs.inventory_order_type(),
        'qs_product_type': qs.product_order_type(),
    }

    template = 'apps/dashboard/order/orders.html'
    return render(request, template, data)

@manager_required
def categories_dashboard(request):

    qs = Category.objects.all()

    data = {

        'qs_count': qs.count(),
    }

    template = 'apps/dashboard/category/categories.html'
    return render(request, template, data)