
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group
from django.http import Http404, HttpResponse
from django.contrib.messages import error, success, info
from django.urls import reverse

# Models
from registration.models import CustomUser
from products.models import Product, ProductItem
from categories.models import Category
from inventories.models import Inventory
from accounts.models import Account
from orders.models import Order

from project.settings import BANNED_GROUP, CLIENT_GROUP, MOD_GROUP, MOD_ROLE, ACTIVE_USER, BANNED_USER, DEFAULT_ROLE, MANAGER_GROUP, MANAGER_ROLE
from decorators.decorators import admin_only

from .forms import (
    ManageCustomUserForm, ManageAccountForm,
    CreateProductForm, ManageProductForm,
    CreateCategoryForm, ManageCategoryForm,
    ManageOrderForm,
    )


# Administration
@admin_only
def administration_view(request):
    ctx = {}

    template = 'administration/administration.html'
    return render(request, template, ctx)


# CustomUser Model Management
@admin_only
def users_view(request):

    qs = CustomUser.objects.all()

    ctx = {'qs':qs}
    template = 'administration/models/customuser/users.html'
    return render(request, template, ctx)

@admin_only
def user_management(request, pk=None):

    obj = get_object_or_404(CustomUser, pk=pk)
    groups = obj.groups.all()

    if request.method == 'POST':

        if int(request.POST.get('customuser:managed')) == pk:

            form = ManageCustomUserForm(request.POST, instance=obj)
            if form.errors:
                for k, e in form.errors.items():
                    error(request, e)

                return HttpResponse(status=200)

            elif form.is_valid():

                form.save()
                success(request, 'Data changes have been saved.')

            else:
                error(request, 'Something went wrong :(')

    else:
        form = ManageCustomUserForm(instance=obj)

    ctx = {'form': form, 'obj': obj, 'groups': groups}
    template = 'administration/models/customuser/user.html'
    return render(request, template, ctx)

@admin_only
def set_banned(request, pk=None):

    obj = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        if request.POST.get('customuser:banned') == str(pk):
            group, created = Group.objects.get_or_create(name=BANNED_GROUP)
            obj.groups.clear()
            group.user_set.add(obj)
            obj.status = BANNED_USER
            obj.save()
            success(request, f'user: {obj.username} became banned, by {request.user.username}')
        else:
            raise Http404

    ctx={'obj':obj}
    template='administration/models/customuser/forms/set_banned.html'
    return render(request, template, ctx)

@admin_only
def set_default(request, pk=None):

    obj = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        if request.POST.get('customuser:default') == str(pk):
            group, created = Group.objects.get_or_create(name=CLIENT_GROUP)
            obj.groups.clear()
            group.user_set.add(obj)
            obj.status = ACTIVE_USER
            obj.role = DEFAULT_ROLE
            obj.is_staff = False
            obj.is_mod = False
            obj.is_manager = False
            obj.save()
            success(request, f'user: {obj.username} became default, by {request.user.username}')
        else:
            raise Http404

    ctx={'obj':obj}
    template='administration/models/customuser/forms/set_default.html'
    return render(request, template, ctx)

@admin_only
def set_mod(request, pk=None):

    obj = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        if request.POST.get('customuser:mod') == str(pk):
            group, created = Group.objects.get_or_create(name=MOD_GROUP)
            group.user_set.add(obj)
            obj.is_mod = True
            obj.role = MOD_ROLE
            obj.save()
            success(request, f'user: {obj.username} became moderator, by {request.user.username}')

        else:
            raise Http404

    ctx={'obj':obj}
    template='administration/models/customuser/forms/set_mod.html'
    return render(request, template, ctx)

@admin_only
def set_manager(request, pk=None):

    obj = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        if request.POST.get('customuser:manager') == str(pk):
            group, created = Group.objects.get_or_create(name=MANAGER_GROUP)
            group.user_set.add(obj)
            obj.is_manager = True
            obj.role = MANAGER_ROLE
            print(MANAGER_ROLE)
            obj.save()
            success(request, f'user: {obj.username} became manager, by {request.user.username}')
        else:
            raise Http404

    ctx={'obj':obj}
    template='administration/models/customuser/forms/set_manager.html'
    return render(request, template, ctx)


# Accounts Model Management
@admin_only
def account_management(request, pk=None):

    obj = get_object_or_404(Account, pk=pk)

    if request.method == 'POST':

        if int(request.POST.get('account:managed')) == pk:

            form = ManageAccountForm(request.POST, instance=obj)
            if form.errors:
                for k, e in form.errors.items():
                    error(request, e)

            elif form.is_valid():
                form.save()
                success(request, 'Data changes have been saved.')

            else:
                error(request, 'Something went wrong :(')

    else:
        form = ManageAccountForm(instance=obj)

    ctx = {'form': form, 'obj': obj}
    template = 'administration/models/account/account.html'
    return render(request, template, ctx)


# Products Model Management
@admin_only
def products_view(request):

    qs = Product.objects.all()

    ctx = {'qs':qs}
    template = 'administration/models/product/products.html'
    return render(request, template, ctx)

@admin_only
def product_management(request, slug=None):

    obj = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        if request.POST.get('product:managed') == slug:

            form = ManageProductForm(request.POST, request.FILES, instance=obj)
            if form.errors:
                for k, e in form.errors.items():
                    error(request, e)
                return HttpResponse(status=200)

            elif form.is_valid():
                form.save()
                success(request, 'Data changes have been saved.')

            else:
                error(request, 'Something went wrong :(')
    else:
        form = ManageProductForm(instance=obj)

    ctx = {'form': form, 'obj': obj}
    template = 'administration/models/product/product.html'
    return render(request, template, ctx)

@admin_only
def create_product(request):

    if request.method == 'POST':

        if request.POST.get('product:created') is not None:
            form = CreateProductForm(request.POST, request.FILES)

            if form.errors:
                for k, e in form.errors.items():
                    error(request, (k, e))
                return HttpResponse(status=200)

            elif form.is_valid():

                product = form.save(commit=False)
                product.author = request.user
                product.save()

                success(request, 'Product created successfully.')

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
        form = CreateProductForm()

    ctx = {'form': form}
    template = 'administration/models/product/create.html'
    return render(request, template, ctx)

@admin_only
def delete_product(request, slug=None):

    obj = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        if request.POST.get('product:deleted') == str(slug):
            obj.delete()

        else:
            error(request, 'Something went wrong :(')

    ctx= {'obj': obj}
    template = 'administration/models/product/delete.html'
    return render(request, template, ctx)


# Categories Model Management
@admin_only
def categories_view(request):

    qs = Category.objects.all()

    ctx = {'qs':qs}
    template = 'administration/models/category/categories.html'
    return render(request, template, ctx)

@admin_only
def category_management(request, slug=None):

    obj = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=obj)

    if request.method == 'POST':
        if request.POST.get('category:managed') == slug:

            form = ManageCategoryForm(request.POST, request.FILES, instance=obj)
            if form.errors:
                for k, e in form.errors.items():
                    error(request, e)

            elif form.is_valid():
                form.save()
                success(request, 'Data changes have been saved.')

            else:
                error(request, 'Something went wrong :(')
    else:
        form = ManageCategoryForm(instance=obj)

    ctx = {'form': form, 'obj': obj, 'products':products}
    template = 'administration/models/category/category.html'
    return render(request, template, ctx)

@admin_only
def create_category(request):

    if request.method == 'POST':

        if request.POST.get('category:created') is not None:
            form = CreateCategoryForm(request.POST, request.FILES)

            if form.errors:
                for k, e in form.errors.items():
                    error(request, (k, e))

            elif form.is_valid():

                category = form.save(commit=False)
                category.author = request.user
                category.save()

                success(request, 'Category created successfully.')

                reverse_url = category.get_absolute_url()
                if request.htmx:
                    headers={
                        'HX-Location': reverse_url
                    }
                    return HttpResponse(f'{request.user.username} Created category named {category.name}.', headers=headers)
                return redirect(reverse_url)

            else:
                error(request, 'Something went wrong (.')
    else:
        form = CreateCategoryForm()

    ctx = {'form': form}
    template = 'administration/models/category/create.html'
    return render(request, template, ctx)

@admin_only
def delete_category(request, slug=None):

    obj = get_object_or_404(Category, slug=slug)

    if request.method == 'POST':
        if request.POST.get('category:deleted') == str(slug):
            obj.delete()

        else:
            error(request, 'Something went wrong :(')

    ctx= {'obj': obj}
    template = 'administration/models/category/delete.html'
    return render(request, template, ctx)


# Categories Model Management
@admin_only
def orders_view(request):

    qs = Order.objects.all()

    ctx = {'qs':qs}
    template = 'administration/models/order/orders.html'
    return render(request, template, ctx)

@admin_only
def client_orders_view(request, client_pk=None):

    client = get_object_or_404(CustomUser, pk=client_pk)
    qs = Order.objects.filter(client = client)

    ctx = {'qs':qs}
    template = 'administration/models/order/orders.html'
    return render(request, template, ctx)

@admin_only
def order_management(request, slug=None):

    obj = get_object_or_404(Order, slug=slug)

    if request.method == 'POST':
        if request.POST.get('order:managed') == slug:

            form = ManageOrderForm(request.POST, instance=obj)
            if form.errors:
                for k, e in form.errors.items():
                    error(request, e)

            elif form.is_valid():
                form.save()
                success(request, 'Data changes have been saved.')

            else:
                error(request, 'Something went wrong :(')
    else:
        form = ManageOrderForm(instance=obj)

    ctx = {'form': form, 'obj': obj}
    template = 'administration/models/order/order.html'
    return render(request, template, ctx)


@admin_only
def delete_order(request, slug=None):

    obj = get_object_or_404(Order, slug=slug)

    if request.method == 'POST':
        if request.POST.get('order:deleted') == str(slug):
            obj.delete()
            success(request, 'Order has been deleted successfully.')

        else:
            error(request, 'Something went wrong :(')

    ctx= {'obj': obj}
    template = 'administration/models/order/delete.html'
    return render(request, template, ctx)