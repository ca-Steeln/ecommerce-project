
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.dispatch import receiver
from django.db.models import Q

from registration.models import CustomUser
from products.models import Product, ProductItem

from .utils import slugify_instance
from .settings import (
    ORDER_STATUS_CHOICES, ORDER_TYPE_CHOICES,
    INVENTORY_ORDER, PRODUCT_ORDER,
    CREATED,
    SHIPPING_METHODS, DEFAULT_SHIPPING_METHOD
    )

# Create your models here.


class OrderQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None:
            return self.none()

        lookups = Q(client__username__icontains=query) | Q(items__products__in=query)
        return self.filter(lookups)

    def inventory_order_type(self):
        return self.filter(order_type=INVENTORY_ORDER)

    def product_order_type(self):
        return self.filter(order_type=PRODUCT_ORDER)

class OrderManager(models.Manager):

    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query=query)

class Order(models.Model):

    client = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, editable=False)

    items = models.ManyToManyField(ProductItem)

    order_type = models.CharField(max_length=128, choices=ORDER_TYPE_CHOICES, editable=False)

    status = models.CharField(max_length=128, choices=ORDER_STATUS_CHOICES, default=CREATED)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    payment_method = models.CharField(max_length=20, null=True)
    transaction_id = models.CharField(max_length=100)

    # price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    unit_price = models.PositiveIntegerField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.PositiveIntegerField(null=True)

    shipping_method = models.CharField(max_length=20, choices=SHIPPING_METHODS, default=DEFAULT_SHIPPING_METHOD)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    note = models.TextField(blank=True, null=True)

    tracking_number = models.CharField(max_length=50, blank=True, null=True)

    slug = models.SlugField(unique=True, blank=True, editable=False)


    objects = OrderManager()


    def get_orders_url(self):
        return reverse("orders:orders", kwargs={"pk": self.client.pk})

    def get_absolute_url(self):
        return reverse("orders:order", kwargs={"pk": self.client.pk, "slug": self.slug})

    def get_manage_url(self):
        return reverse("administration:order", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("administration:order-delete", kwargs={"slug": self.slug})

    def get_abort_url(self):
        return reverse("orders:abort", kwargs={"pk": self.client.pk, "slug": self.slug})




@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance(instance, save=False)

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance(instance, save=True)
