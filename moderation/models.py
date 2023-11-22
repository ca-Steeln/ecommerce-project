
from django.db import models
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.db.models import Q
from django.db import models

from decorators.decorators import admin_only, group_required
from accounts.models import Account
from products.models import Product, ProductItem
from orders.models import Order
from categories.models import Category
from inventories.models import Inventory
from registration.models import CustomUser

from project.settings import (
    CLIENT_GROUP, BANNED_GROUP, MOD_GROUP, ADMIN_GROUP,
    DEFAULT_ROLE, MOD_ROLE, ADMIN_ROLE,
    ACTIVE_USER, BANNED_USER, DELETED_USER
    )

# Create your views here.

class UsersQuertSet(models.QuerySet):
    def search(self, query=None):
        if query is None:
            return self.none()

        lookups = Q(username__icontains=query) | Q(id__icontains=query)
        return self.filter(lookups)

class UsersManager(models.Manager):

    def get_queryset(self):
        return UsersQuertSet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query=query)

class UsersManagement(models.Model):

    objects = UsersManager()

class DashboardManagement():


    def get_groups(self):
        client, created = Group.objects.get_or_create(name=CLIENT_GROUP)
        banned, created = Group.objects.get_or_create(name=BANNED_GROUP)
        mod, created = Group.objects.get_or_create(name=MOD_GROUP)
        admin, created = Group.objects.get_or_create(name=ADMIN_GROUP)

    def users_db_managment(self):
        client_g, created = Group.objects.get_or_create(name=CLIENT_GROUP)
        banned_g, created = Group.objects.get_or_create(name=BANNED_GROUP)
        mod_g, created = Group.objects.get_or_create(name=MOD_GROUP)
        admin_g, created = Group.objects.get_or_create(name=ADMIN_GROUP)

        data = {

            # user objects
            'users': CustomUser.objects.all(),

            # group objects
            'client_group': client_g.user_set.all(),
            'banned_group': banned_g.user_set.all(),
            'mod_group': mod_g.user_set.all(),
            'admin_group': admin_g.user_set.all(),

            # Roles
            'default_role': CustomUser.objects.filter(role=DEFAULT_ROLE),
            'mod_role': CustomUser.objects.filter(role=MOD_ROLE),
            'admin_role': CustomUser.objects.filter(role=ADMIN_ROLE),

            # Status
            'active_status': CustomUser.objects.filter(status=ACTIVE_USER),
            'banned_status': CustomUser.objects.filter(status=BANNED_USER),
            'deleted_status': CustomUser.objects.filter(role=DELETED_USER),
        }

        return data



