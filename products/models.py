
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from categories.models import Category
from .utils import slugify_instance
# Create your models here.

class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True) # need a test
    name = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=5000)
    adminPrice = models.DecimalField(max_digits=10, decimal_places=2)
    clientPrice = models.DecimalField(max_digits=10, decimal_places=2)
    vistorPrice = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    discount = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def default_category(instance):
        return instance.category

    def directory_path(instance, filename):
        return f"products/product_{instance.id}/{filename}"

    def default_directory_path():
        return "products/default/products-default-icon.jpg"
    image = models.ImageField(upload_to= directory_path, default=default_directory_path, blank=True, null=True)


    def __str__(self) -> str:
        return self.title

    # reverse urls

    def get_product_url(self):
        return reverse("products:product", kwargs={"category_name": self.category.name, "slug": self.slug})


    def get_update_url(self):
        return reverse("products:update", kwargs={"category_name": self.category.name, "slug": self.slug})

    def get_delete_url(self):
        return reverse("products:delete", kwargs={"category_name": self.category.name, "slug": self.slug})


def product_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance(instance, save=False)
pre_save.connect(product_pre_save, sender=Product)

def product_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance(instance, save=True)
post_save.connect(product_post_save, sender=Product)