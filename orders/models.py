
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.dispatch import receiver

from products.models import Product

from .utils import slugify_instance
from .settings import ORDER_STATUS_CHOICES
# Create your models here.

class Order(models.Model):

    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(Product)
    status = models.CharField(max_length=128, choices=ORDER_STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def get_orders_url(self):
        return reverse("orders:orders", kwargs={"client_pk": self.client.pk})

    def get_order_url(self):
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


