
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.dispatch import receiver

from products.models import Product, ProductItem

from .utils import slugify_instance
from .settings import ORDER_STATUS_CHOICES, ORDER_TYPE_CHOICES, CREATED
# Create your models here.


class Order(models.Model):

    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)

    items = models.ManyToManyField(ProductItem)

    order_type = models.CharField(max_length=128, choices=ORDER_TYPE_CHOICES, editable=False)

    status = models.CharField(max_length=128, choices=ORDER_STATUS_CHOICES, default=CREATED)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    payment_method = models.CharField(max_length=20, null=True)
    transaction_id = models.CharField(max_length=100, null=True)

    # price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    unit_price = models.PositiveIntegerField(editable=False,  null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, editable=False,  null=True)
    total_amount = models.PositiveIntegerField(editable=False,  null=True)

    shipping_method = models.CharField(max_length=20, blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    tracking_number = models.CharField(max_length=50, blank=True, null=True)

    slug = models.SlugField(unique=True, blank=True, editable=False)


    def get_orders_url(self):
        return reverse("orders:orders", kwargs={"client_pk": self.client.pk})

    def get_absolute_url(self):
        return reverse("orders:order", kwargs={"client_pk": self.client.pk, "slug": self.slug})

    def get_abort_url(self):
        return reverse("orders:abort", kwargs={"client_pk": self.client.pk, "slug": self.slug})


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance(instance, save=False)

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance(instance, save=True)
