
from django.db import models
from django.urls import reverse

from products.models import ProductItem
from registration.models import CustomUser
# Create your models here.


class Inventory(models.Model):

    client = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, unique=True)
    items = models.ManyToManyField(ProductItem)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("inventories:inventory", kwargs={"pk": self.client.pk})

    def get_clear_url(self):
        return reverse("inventories:clear", kwargs={"pk": self.client.pk})

    def get_order_url(self):
        return reverse("inventories:order", kwargs={"pk": self.client.pk})


    def __str__(self) -> str:
        return f'{self.client} | {self.items.count()} | {self.created_at.date()} / {self.updated_at.date()}'