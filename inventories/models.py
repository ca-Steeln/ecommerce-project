
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from products.models import Product

# Create your models here.

class Inventory(models.Model):

    client = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, unique=True)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_inventory_url(self):
        return reverse("inventories:inventory", kwargs={"client_pk": self.client.pk})

    def get_clear_url(self):
        return reverse("inventories:clear", kwargs={"client_pk": self.client.pk})

    def get_order_url(self):
        return reverse("inventories:order", kwargs={"client_pk": self.client.pk})