
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import error, success
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse

from registration.models import CustomUser
from products.models import Product
from decorators.decorators import admin_only

from .models import Category
from .forms import CreateCategoryForm, UpdateCategoryForm


# Create your views here.


def categories_view(request):
    ctx = {}
    qs = Category.objects.filter(active=True)

    ctx['qs'] = qs
    template = 'apps/categories/categories.html'
    return render(request, template, ctx)


def category_view(request, slug=None):

    obj = get_object_or_404(Category, slug=slug)

    qs = Product.objects.filter(category=obj, active=True)

    ctx = {'obj':obj, 'qs': qs}
    template = 'apps/categories/category.html'
    return render(request, template, ctx)


@admin_only
def create_category(request):
    ctx = {}

    if request.method == 'POST':

        if request.POST.get('categories:create') is not None:
            form = CreateCategoryForm(request.POST, request.FILES)

            if form.errors:
                for k, e in form.errors.items():
                    error(request, e)

            elif form.is_valid():

                category = form.save(commit=False)
                category.author = request.user
                category.save()
                ctx['obj'] = category

                # htmx request need to be dynamic redirect

                reverse_url = category.get_absolute_url()
                if request.htmx:
                    headers={
                        'HX-Location': reverse_url
                    }
                    return HttpResponse(f'{request.user.username} Created category named {category.name or category.title}.', headers=headers)
                return redirect(reverse_url)

            else:
                error(request, 'Something went wrong :(')
    else:
        form = CreateCategoryForm()

    ctx['form'] = form
    template = 'apps/categories/create.html'
    return render(request, template, ctx)


@admin_only
def update_category(request, slug=None):
    ctx = {}

    obj = get_object_or_404(Category, slug=slug)

    if request.method == 'POST':

        if request.POST.get('categories:update') is not None:

            form = UpdateCategoryForm(request.POST, request.FILES, instance=obj)

            if form.errors:
                for k, e in form.errors.items():
                    error(request, e)

            elif form.is_valid():
                category = form.save(commit=False)
                category.author = request.user
                category.save()
                ctx['obj'] = category

                reverse_url = category.get_absolute_url()
                if request.htmx:
                    headers={
                        'HX-Location': reverse_url
                    }
                    return HttpResponse(f'{request.user.username} Updated Category named {obj.name or obj.title}.', headers=headers)
                return redirect(reverse_url)

            else:
                error(request, 'Something went wrong :(')

    else:
        form = UpdateCategoryForm(instance= obj)

    ctx['form'] = form
    ctx['obj'] = obj

    template = 'apps/categories/update.html'
    return render(request, template, ctx)


@admin_only
def delete_category(request, slug=None):


    ctx = {}
    user = get_object_or_404(CustomUser, id=request.user.id)
    obj = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        if request.POST.get('categories:delete') is not None:
            if not user.is_superuser:
                raise Http404

            obj.delete()

            reverse_url = reverse('categories:categories')
            if request.htmx:
                headers={
                        'HX-Location': reverse_url
                    }
                return HttpResponse(f'{user.username} Deleted Category named {obj.name or obj.title}.', headers=headers)
            return redirect(reverse_url)

    ctx['obj'] = obj
    template = 'apps/categories/delete.html'
    return render(request, template, ctx)

